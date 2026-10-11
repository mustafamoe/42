"""Private regressions for the supplied evaluation screenshot requirements."""

import json
import os
import random
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

import numpy as np
from pydantic import ValidationError

from src.decoder import COPY_LOGIT_BONUS, Decoder, literal_source, load_decoder
from src.grammar import ScalarGrammar
from src.schema import Call, Function, Parameter, number_as_float, validate_call


class EvaluationTests(unittest.TestCase):
    """Verify allowed values, refusal, numeric precision and SDK storage."""

    def test_ranked_selection_matches_exhaustive_masking(self):
        vocabulary = dict(enumerate([
            b'"', b'hello', b'Hello', b'"}', b'"hello"}', b'"Hello"}',
            b"'\"}", b'\\', b'\\\\d+', b'\\n', b'1', b'2', b'0', b'.',
            b'true}', b'false}', b'null}', b'"utf-8"}', b'"latin-1"}',
            b'invalid', b'\xc3', b'\xa9', b' ', b'}',
        ]))
        source, boundaries = literal_source('Keep hello and café\\n exactly')
        copied = ScalarGrammar(
            kind="string", delimiter="}", source=source,
            boundaries=boundaries,
        )
        cases = [(copied, raw) for raw in (b'', b'"', b'"hello', b'"\\')]
        cases += [(ScalarGrammar(kind=kind, delimiter="}"), raw)
                  for kind, raw in (
                      ("number", b''), ("number", b'1.'),
                      ("integer", b''), ("boolean", b''), ("null", b''),
                  )]
        cases.append((ScalarGrammar(
            kind="string", delimiter="}",
            choices=(b'"utf-8"}', b'"latin-1"}'),
        ), b''))
        rng = random.Random(42)
        sdk = Mock()
        decoder = Decoder(model=sdk, vocabulary=vocabulary)
        for grammar, raw in cases:
            syntax = ScalarGrammar(
                kind=grammar.kind, delimiter=grammar.delimiter,
                choices=grammar.choices,
            )
            for pending in (False, True):
                for _ in range(40):
                    scores = [rng.choice([
                        -5, -3.5, -1, 0, 1, 3.5, 5, float('nan'),
                        float('inf'), -float('inf'),
                    ]) for _ in range(len(vocabulary) + 2)]
                    sdk.get_logits_from_input_ids.return_value = scores
                    legal = {
                        index: score for index, score in enumerate(scores)
                        if (index in vocabulary and np.isfinite(score)
                            and syntax.status(raw + vocabulary[index]) >= 0)
                    }
                    if not legal:
                        with self.assertRaises(ValueError):
                            decoder.select_token([42], raw, grammar, pending)
                        continue
                    best = min(legal, key=lambda index: (-legal[index], index))
                    apply_copy = grammar.source is not None
                    if apply_copy and pending:
                        insensitive = grammar.model_copy(update={
                            "source": grammar.source.lower(),
                        })
                        apply_copy = insensitive.copy_at_boundary(
                            (raw + vocabulary[best]).lower(),
                        )
                    if apply_copy:
                        legal = {
                            index: score + (COPY_LOGIT_BONUS if
                                grammar.copy_at_boundary(raw + vocabulary[index])
                                else 0)
                            for index, score in legal.items()
                        }
                    expected = min(
                        legal, key=lambda index: (-legal[index], index),
                    )
                    self.assertEqual(decoder.select_token(
                        [42], raw, grammar, pending,
                    ), expected)

    def test_ordinary_arguments_keep_the_original_tool_context(self):
        functions = [Function.model_validate({
            "name": name, "description": description,
            "parameters": {"text": {"type": "string"}},
            "returns": {"type": "null"},
        }) for name, description in (
            ("store_note", "Store a note verbatim"),
            ("reverse_text", "Reverse a string"),
        )]
        sdk = Mock()
        sdk.encode.return_value.tolist.return_value = [[42]]
        decoder = Decoder(model=sdk, vocabulary={0: b'"note"}'})
        prompt = 'Store the note "hello".'
        with patch.object(Decoder, "reason"), patch.object(
            Decoder, "generate", side_effect=["store_note", "hello"],
        ):
            call = decoder.call(prompt, functions)
        contexts = [item.args[0] for item in sdk.encode.call_args_list
                    if "<tools>\n" in item.args[0]]
        tools = [
            [json.loads(line)["function"]["name"]
             for line in context.split("<tools>\n")[1].split("\n</tools>")[0].splitlines()]
            for context in contexts
        ]
        self.assertEqual(tools[0], [
            "store_note", "reverse_text", "no_matching_function",
        ])
        self.assertEqual(len(tools), 1)
        self.assertTrue(all(prompt in context for context in contexts))
        self.assertEqual(call.prompt, prompt)
        self.assertEqual(call.name, "store_note")
        self.assertEqual(call.parameters, {"text": "hello"})

    def test_boundary_metadata_preserves_literal_requests(self):
        sdk = Mock()
        sdk.encode.return_value.tolist.return_value = [[42]]
        decoder = Decoder(model=sdk, vocabulary={0: b'false,'})
        prompt = 'Store the literal message "LAUNCH body FINISH".'
        with patch.object(Decoder, "reason"), patch.object(
            Decoder, "generate", return_value=False,
        ) as generate:
            self.assertEqual(decoder.argument_request(prompt), prompt)
        self.assertEqual(generate.call_count, 0)

    def test_arbitrary_model_selected_boundaries_keep_content_bytes(self):
        sdk = Mock()
        sdk.encode.return_value.tolist.return_value = [[42]]
        decoder = Decoder(model=sdk, vocabulary={0: b'"label"}'})
        cases = [
            ('Between LAUNCH and FINISH: LAUNCH café "hello" \\path FINISH',
             'LAUNCH', 'FINISH', 'café "hello" \\path'),
            ('Inside <note> and </note>: <note> first\nsecond </note>',
             '<note>', '</note>', ' first\nsecond '),
            ('Between markers: OPEN  spaced  CLOSE',
             'OPEN', 'CLOSE', ' spaced '),
            ('Store "my note" between GO and DONE: GO a "quoted" body DONE',
             'GO', 'DONE', 'a "quoted" body'),
        ]
        for prompt, opening, closing, content in cases:
            with self.subTest(prompt=prompt), patch.object(
                Decoder, "reason",
            ), patch.object(Decoder, "generate", side_effect=[
                opening, closing,
            ]):
                request = decoder.argument_request(prompt)
            self.assertEqual(request.split(':\n', 1)[1], content)
            if prompt.startswith('Store "my note"'):
                self.assertEqual(request, 'Store "my note":\na "quoted" body')

    def test_unlocatable_boundary_metadata_fails_clearly(self):
        sdk = Mock()
        sdk.encode.return_value.tolist.return_value = [[42]]
        decoder = Decoder(model=sdk, vocabulary={0: b'"label"}'})
        with patch.object(Decoder, "reason"), patch.object(
            Decoder, "generate", side_effect=['absent', 'missing'],
        ), self.assertRaisesRegex(ValueError, "selected text boundaries"):
            decoder.argument_request('Between markers: OPEN body CLOSE')

    def test_enum_validates_exact_types_and_membership(self):
        for kind, values in (
            ("string", ["utf-8", "latin-1"]),
            ("number", [1, 2.5]),
            ("integer", [1, 2]),
            ("boolean", [True]),
            ("null", [None]),
        ):
            parameter = Parameter(type=kind, enum=values)
            for value in values:
                self.assertTrue(parameter.accepts(value))
            self.assertFalse(parameter.accepts("unlisted"))
        number = Parameter(type="number", enum=[1])
        self.assertTrue(number.accepts(1.0))
        self.assertFalse(number.accepts(True))

    def test_invalid_enum_definitions_are_rejected(self):
        for data in (
            {"type": "string", "enum": []},
            {"type": "number", "enum": [True]},
            {"type": "integer", "enum": [1.0]},
            {"type": "boolean", "enum": [1]},
            {"type": "string", "enum": [None]},
            {"type": "number", "enum": [float("inf")]},
            {"type": "number", "enum": [float("nan")]},
        ):
            with self.subTest(data=data), self.assertRaises(ValidationError):
                Parameter.model_validate(data)

    def test_literal_copy_preserves_every_source_substring_and_byte_prefix(self):
        text = 'a "quoted" \\path\n café عربي 😀 {item}'
        source, boundaries = literal_source(text)
        grammar = ScalarGrammar(
            kind="string", delimiter="}", source=source,
            boundaries=boundaries,
        )
        for start in range(len(text) + 1):
            for end in range(start, len(text) + 1):
                raw = (json.dumps(text[start:end], ensure_ascii=False)
                       + "}").encode()
                for index in range(len(raw)):
                    self.assertEqual(grammar.status(raw[:index]), 0)
                self.assertEqual(grammar.status(raw), 1)

    def test_literal_copy_rejects_invented_text_and_escape_fragments(self):
        source, boundaries = literal_source('Say "hello" to {name} \\n')
        grammar = ScalarGrammar(
            kind="string", delimiter="}", source=source,
            boundaries=boundaries,
        )
        for value in ('Say \'hello\' to {name}', 'Say "hello" to {name}"', '\n'):
            raw = (json.dumps(value, ensure_ascii=False) + "}").encode()
            self.assertEqual(grammar.status(raw), -1)

    def test_literal_copy_prefers_source_over_a_small_punctuation_difference(self):
        sdk = Mock()
        sdk.encode.return_value.tolist.return_value = [[42]]
        sdk.get_logits_from_input_ids.side_effect = [
            [10, 0, 0, 0], [0, 10, 0, 0], [0, 0, 4, 3],
        ]
        source, boundaries = literal_source('Keep hello exactly')
        decoder = Decoder(model=sdk, vocabulary={
            0: b'"', 1: b'hello', 2: b"'\"}", 3: b'"}',
        })
        result = decoder.generate([], ScalarGrammar(
            kind="string", delimiter="}", source=source,
            boundaries=boundaries,
        ))
        self.assertEqual(result, 'hello')

    def test_copy_preference_does_not_reward_an_unfinished_escape(self):
        sdk = Mock()
        sdk.get_logits_from_input_ids.return_value = [3, 4]
        source, boundaries = literal_source('Replace digits in "text"')
        decoder = Decoder(model=sdk, vocabulary={
            0: b'\\', 1: b'\\\\d+',
        })
        token = decoder.select_token([42], b'"', ScalarGrammar(
            kind="string", delimiter="}", source=source,
            boundaries=boundaries,
        ))
        self.assertEqual(token, 1)

    def test_pending_copy_preserves_original_case_of_the_model_selected_word(self):
        sdk = Mock()
        sdk.get_logits_from_input_ids.return_value = [4, 3]
        source, boundaries = literal_source('Greet shrek')
        decoder = Decoder(model=sdk, vocabulary={
            0: b'Shrek"}', 1: b'shrek"}',
        })
        token = decoder.select_token([42], b'"', ScalarGrammar(
            kind="string", delimiter="}", source=source,
            boundaries=boundaries,
        ), copy_pending=True)
        self.assertEqual(token, 1)

    def test_pending_copy_does_not_promote_literals_over_a_derived_start(self):
        sdk = Mock()
        sdk.get_logits_from_input_ids.return_value = [4, 3]
        source, boundaries = literal_source('Replace digits in "34"')
        decoder = Decoder(model=sdk, vocabulary={
            0: b'\\\\d+', 1: b'34',
        })
        token = decoder.select_token([42], b'"', ScalarGrammar(
            kind="string", delimiter="}", source=source,
            boundaries=boundaries,
        ), copy_pending=True)
        self.assertEqual(token, 0)

    def test_derived_string_prefix_can_generate_a_pattern_absent_from_source(self):
        sdk = Mock()
        sdk.encode.return_value.tolist.return_value = [[42]]
        sdk.get_logits_from_input_ids.side_effect = [
            [10, 0, 0], [0, 10, 0], [0, 0, 10],
        ]
        source, boundaries = literal_source('Replace all digit runs')
        decoder = Decoder(model=sdk, vocabulary={
            0: b'"', 1: b'\\\\d+', 2: b'"}',
        })
        result = decoder.generate([], ScalarGrammar(
            kind="string", delimiter="}", source=source,
            boundaries=boundaries,
        ))
        self.assertEqual(result, '\\d+')

    def test_derived_string_can_extend_a_prefix_present_in_source(self):
        sdk = Mock()
        sdk.encode.return_value.tolist.return_value = [[42]]
        sdk.get_logits_from_input_ids.side_effect = [
            [10, 0, 0, 0], [0, 10, 0, 0], [0, 0, 10, 3], [0, 0, 0, 10],
        ]
        source, boundaries = literal_source('Replace cat followed by digits')
        decoder = Decoder(model=sdk, vocabulary={
            0: b'"', 1: b'cat', 2: b'\\\\d+', 3: b'"}',
        })
        result = decoder.generate([], ScalarGrammar(
            kind="string", delimiter="}", source=source,
            boundaries=boundaries,
        ))
        self.assertEqual(result, 'cat\\d+')

    def test_enum_masks_a_higher_logit_for_an_unlisted_value(self):
        sdk = Mock()
        sdk.encode.return_value.tolist.return_value = [[42]]
        sdk.get_logits_from_input_ids.return_value = [100, 3, 2]
        decoder = Decoder(model=sdk, vocabulary={
            0: b'"ascii"}', 1: b'"utf-8"}', 2: b'"latin-1"}',
        })
        value = decoder.generate([], ScalarGrammar(
            kind="string", delimiter="}",
            choices=(b'"utf-8"}', b'"latin-1"}'),
        ))
        self.assertEqual(value, "utf-8")

    def test_final_validation_rejects_an_unlisted_argument(self):
        function = Function.model_validate({
            "name": "read_document", "description": "Read a document",
            "parameters": {
                "encoding": {"type": "string", "enum": ["utf-8"]},
            },
            "returns": {"type": "string"},
        })
        with self.assertRaisesRegex(ValueError, "allowed values"):
            validate_call(Call(prompt="read", name=function.name,
                               parameters={"encoding": "ascii"}), function)

    def test_number_conversion_preserves_precision_and_large_values(self):
        for value in (0, -42, 2**53, 2**100):
            result = number_as_float(value)
            self.assertIs(type(result), float)
            self.assertEqual(int(result), value)
        for value in (2**53 + 1, 10**100, 10**400):
            result = number_as_float(value)
            self.assertIs(type(result), int)
            self.assertEqual(result, value)

    def test_model_can_reject_instead_of_selecting_an_unrelated_function(self):
        sdk = Mock()
        sdk.encode.return_value.tolist.return_value = [[42]]
        sdk.get_logits_from_input_ids.return_value = [3, 2]
        decoder = Decoder(model=sdk, vocabulary={
            0: b'"no_matching_function",', 1: b'"greet",',
        })
        function = Function.model_validate({
            "name": "greet", "description": "Greet a person",
            "parameters": {}, "returns": {"type": "string"},
        })
        with patch.object(Decoder, "reason"), self.assertRaisesRegex(
            ValueError, "No available function matches",
        ):
            decoder.call("A request with no available tool", [function])
        sdk.get_logits_from_input_ids.assert_called_once()

    def test_rejection_tool_does_not_hide_a_supplied_function_with_its_name(self):
        sdk = Mock()
        sdk.encode.return_value.tolist.return_value = [[42]]
        sdk.get_logits_from_input_ids.return_value = [10, 2]
        decoder = Decoder(model=sdk, vocabulary={
            0: b'"no_matching_function",', 1: b'"_no_matching_function",',
        })
        function = Function.model_validate({
            "name": "no_matching_function", "description": "An available tool",
            "parameters": {}, "returns": {"type": "null"},
        })
        with patch.object(Decoder, "reason"):
            call = decoder.call("Run the available tool", [function])
        self.assertEqual(call.name, "no_matching_function")
        self.assertEqual(call.parameters, {})
        sdk.get_logits_from_input_ids.return_value = [2, 10]
        with patch.object(Decoder, "reason"), self.assertRaisesRegex(
            ValueError, "No available function matches",
        ):
            decoder.call("An unrelated request", [function])

    def test_number_conversion_does_not_change_integer_or_boolean(self):
        sdk = Mock()
        sdk.encode.return_value.tolist.return_value = [[42]]
        decoder = Decoder(model=sdk, vocabulary={0: b"x"})
        function = Function.model_validate({
            "name": "record", "description": "Record typed values",
            "parameters": {
                "amount": {"type": "number"},
                "count": {"type": "integer"},
                "enabled": {"type": "boolean"},
            },
            "returns": {"type": "null"},
        })
        with patch.object(Decoder, "reason"), patch.object(
            Decoder, "generate", side_effect=["record", 2, 3, True],
        ):
            result = decoder.call("record", [function])
        self.assertIs(type(result.parameters["amount"]), float)
        self.assertIs(type(result.parameters["count"]), int)
        self.assertIs(type(result.parameters["enabled"]), bool)

    def test_sdk_cache_is_a_real_local_directory_before_loading(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            vocabulary = root / "vocab.json"
            vocabulary.write_text(json.dumps({"x": 0}))
            sdk = Mock()
            sdk.get_path_to_vocab_file.return_value = str(vocabulary)
            local = root / "model"

            def create_model(**kwargs):
                self.assertTrue(local.is_dir())
                self.assertEqual(os.environ["HF_HUB_CACHE"], str(local.resolve()))
                self.assertEqual(kwargs, {"trust_remote_code": False})
                return sdk

            module = SimpleNamespace(Small_LLM_Model=create_model)
            with patch.dict(os.environ), patch.dict(
                "sys.modules", {"llm_sdk": module},
            ), patch("src.decoder.MODEL_DIRECTORY", local):
                decoder = load_decoder()
            self.assertEqual(decoder.vocabulary, {0: b"x"})


if __name__ == "__main__":
    unittest.main()
