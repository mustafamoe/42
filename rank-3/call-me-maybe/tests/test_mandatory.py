"""Private offline checks; run from submission with unittest discovery."""

import json
import random
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import numpy as np
from pydantic import ValidationError

from src.__main__ import write_calls
from src.decoder import Decoder, vocabulary_bytes
from src.grammar import ScalarGrammar
from src.schema import Call, Function, load_inputs, read_json, validate_call


class GrammarTests(unittest.TestCase):
    """Test prefixes at every byte boundary, including split escape sequences."""

    def test_valid_values_at_every_boundary(self):
        cases = {
            "string": ["", "hello", 'a"b\\c\n\t', "café عربي 😀", "\x00"],
            "number": [0, -42, 2.5, 1e-20, 1.79e308, 12345678901234567890],
            "integer": [0, -42, 12345678901234567890],
            "boolean": [True, False],
            "null": [None],
        }
        for kind, values in cases.items():
            for value in values:
                for ascii_only in (False, True):
                    for delimiter in (",", "}"):
                        grammar = ScalarGrammar(kind=kind, delimiter=delimiter)
                        raw = (json.dumps(value, ensure_ascii=ascii_only)
                               + delimiter).encode()
                        with self.subTest(kind=kind, raw=raw):
                            for index in range(len(raw)):
                                self.assertEqual(grammar.status(raw[:index]), 0)
                            self.assertEqual(grammar.status(raw), 1)

    def test_invalid_scalar_forms(self):
        cases = {
            "string": [b'hello', b'"a\n', b'"\\q', b'"\\uXY', b'"\xff',
                       b'"\xc3x', b'"ok"x', b'"x",garbage', b'null,'],
            "number": [b'01', b'+1', b'NaN', b'Infinity', b'1.e', b'1..',
                       b'--1', b'1e309,', b'1e,', b'"2",', b'true,'],
            "integer": [b'1.2', b'1e2', b'false,', b'01,'],
            "boolean": [b'True', b'0,', b'falsex', b'"true",'],
            "null": [b'None', b'0,', b'nullx'],
        }
        for kind, values in cases.items():
            grammar = ScalarGrammar(kind=kind, delimiter=",")
            for value in values:
                with self.subTest(kind=kind, value=value):
                    self.assertEqual(grammar.status(value), -1)

    def test_random_string_prefixes(self):
        rng = random.Random(42)
        alphabet = 'a"\\\n\r\t\x00éم😀,}'
        grammar = ScalarGrammar(kind="string", delimiter="}")
        for _ in range(80):
            value = "".join(rng.choices(alphabet, k=rng.randrange(40)))
            raw = (json.dumps(value, ensure_ascii=False) + "}").encode()
            self.assertEqual(grammar.status(raw), 1)
            for index in range(len(raw)):
                self.assertEqual(grammar.status(raw[:index]), 0)

    def test_enum_shares_prefix_and_rejects_unknown_name(self):
        grammar = ScalarGrammar(
            kind="string", delimiter=",", choices=(b'"foo",', b'"foobar",')
        )
        self.assertEqual(grammar.status(b'"foo'), 0)
        self.assertEqual(grammar.status(b'"foo",'), 1)
        self.assertEqual(grammar.status(b'"foobar",'), 1)
        self.assertEqual(grammar.status(b'"food",'), -1)

    def test_mask_rejects_highest_logit_and_updates_context(self):
        sdk = Mock()
        sdk.encode.return_value.tolist.return_value = [[42]]
        contexts = []
        def scores(ids):
            contexts.append(ids.copy())
            return [100, 3, -1] if len(contexts) == 1 else [100, -1, 3]
        sdk.get_logits_from_input_ids.side_effect = scores
        decoder = Decoder(model=sdk, vocabulary={0: b'oops', 1: b'12', 2: b','})
        self.assertEqual(decoder.generate(
            [42], ScalarGrammar(kind="number", delimiter=",")
        ), 12)
        self.assertEqual(contexts, [[42], [42, 1]])

    def test_multi_character_token_closes_value(self):
        sdk = Mock()
        sdk.encode.return_value.tolist.return_value = [[42]]
        sdk.get_logits_from_input_ids.return_value = [100, 3]
        decoder = Decoder(model=sdk, vocabulary={0: b'"x",extra', 1: b'"x",'})
        self.assertEqual(decoder.generate(
            [42], ScalarGrammar(kind="string", delimiter=","), '"value":'
        ), "x")
        sdk.encode.assert_called_once_with('"value":')

    def test_whole_empty_string_token_is_not_excluded(self):
        sdk = Mock()
        sdk.encode.return_value.tolist.return_value = [[42]]
        sdk.get_logits_from_input_ids.return_value = [10, 1]
        decoder = Decoder(model=sdk, vocabulary={0: b'""}', 1: b'"x"}'})
        value = decoder.generate([42], ScalarGrammar(kind="string", delimiter="}"), '"text": ')
        self.assertEqual(value, "")

    def test_no_valid_or_finite_token(self):
        sdk = Mock()
        sdk.encode.return_value.tolist.return_value = [[42]]
        decoder = Decoder(model=sdk, vocabulary={0: b'12,'})
        for logits in ([float("nan")], [float("inf")], [-float("inf")], []):
            sdk.get_logits_from_input_ids.return_value = logits
            with self.assertRaises(ValueError):
                decoder.generate([], ScalarGrammar(kind="number", delimiter=","))

    def test_generation_limit_does_not_fabricate_completion(self):
        sdk = Mock()
        sdk.encode.return_value.tolist.return_value = [[42]]
        sdk.get_logits_from_input_ids.return_value = [1]
        decoder = Decoder(model=sdk, vocabulary={0: b'1'})
        with self.assertRaisesRegex(ValueError, "256"):
            decoder.generate([], ScalarGrammar(kind="number", delimiter=","))

    def reasoning_decoder(self, logits):
        sdk = Mock()
        tokens = {"</think>": [2], "<|im_end|>": [3],
                  "\n\n<tool_call>\n": [4]}
        sdk.encode.side_effect = lambda text: np.asarray([tokens[text]])
        sdk.get_logits_from_input_ids.return_value = logits
        return Decoder(model=sdk, vocabulary={0: b"x"})

    def test_reasoning_stops_and_excludes_conversation_end(self):
        decoder = self.reasoning_decoder([0, 5, 1, 100])
        decoder.model.get_logits_from_input_ids.side_effect = [
            [0, 5, 1, 100], [0, 1, 5, 100],
        ]
        context = []
        decoder.reason(context)
        self.assertEqual(context, [1, 2, 4])

    def test_reasoning_limit_returns_to_tool_call(self):
        decoder = self.reasoning_decoder([0, 5, 1, 100])
        context = []
        decoder.reason(context)
        self.assertEqual(context, [1] * 56 + [2, 4])

    def test_reasoning_rejects_nonfinite_logits(self):
        decoder = self.reasoning_decoder([float("nan")] * 4)
        with self.assertRaisesRegex(ValueError, "finite"):
            decoder.reason([])


class FileTests(unittest.TestCase):
    """Check input validation and safe CLI failure without loading the model."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.definitions = self.root / "functions.json"
        self.prompts = self.root / "prompts.json"
        self.output = self.root / "output.json"
        self.function = {
            "name": "anything", "description": "A new test function",
            "parameters": {"value": {"type": "number"}},
            "returns": {"type": "number"},
        }
        self.definitions.write_text(json.dumps([self.function]))
        self.prompts.write_text('[{"prompt":""}]')

    def cli(self, *extra):
        return subprocess.run(
            [sys.executable, "-m", "src", "--functions_definition",
             str(self.definitions), "--input", str(self.prompts),
             "--output", str(self.output), *extra],
            text=True, capture_output=True, timeout=20,
        )

    def test_empty_prompt_preserved(self):
        functions, prompts = load_inputs(self.definitions, self.prompts)
        self.assertEqual(functions[0].name, "anything")
        self.assertEqual(prompts[0].prompt, "")

    def test_wrong_types_and_unknown_keys_rejected(self):
        for data in ([{"prompt": 2}], [{"prompt": "x", "extra": 1}], {}, [None]):
            self.prompts.write_text(json.dumps(data))
            with self.assertRaises(ValidationError):
                load_inputs(self.definitions, self.prompts)

    def test_duplicate_names_and_empty_functions(self):
        for data in ([], [self.function, self.function]):
            self.definitions.write_text(json.dumps(data))
            with self.assertRaises(ValueError):
                load_inputs(self.definitions, self.prompts)

    def test_nested_schema_rejected_clearly(self):
        self.function["parameters"]["value"]["type"] = "object"
        self.definitions.write_text(json.dumps([self.function]))
        with self.assertRaises(ValidationError):
            load_inputs(self.definitions, self.prompts)

    def test_invalid_json_and_missing_file(self):
        for raw in ('[{', '{"a":1,"a":2}', '[NaN]', '[Infinity]', '\ud800'):
            self.prompts.write_bytes(raw.encode("utf-8", errors="surrogatepass"))
            with self.assertRaises(ValueError):
                read_json(self.prompts)
        self.prompts.unlink()
        result = self.cli()
        self.assertEqual(result.returncode, 1)
        self.assertIn("Cannot read", result.stderr)
        self.assertNotIn("Traceback", result.stderr)
        self.assertNotIn("Loading", result.stderr)

    def test_empty_batch_writes_json_without_model(self):
        self.prompts.write_text("[]")
        result = self.cli()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(self.output.read_text()), [])
        self.assertNotIn("Loading", result.stderr)

    def test_bad_input_preserves_existing_output(self):
        self.output.write_text("previous output")
        self.prompts.write_text("bad json")
        result = self.cli()
        self.assertEqual(result.returncode, 1)
        self.assertEqual(self.output.read_text(), "previous output")

    def test_refuses_input_overwrite(self):
        result = self.cli("--output", str(self.prompts))
        self.assertEqual(result.returncode, 1)
        self.assertIn("must not overwrite", result.stderr)

    def test_output_failure_is_graceful(self):
        self.prompts.write_text("[]")
        self.output.mkdir()
        result = self.cli()
        self.assertEqual(result.returncode, 1)
        self.assertNotIn("Traceback", result.stderr)
        self.assertEqual(list(self.root.glob(".function-calls-*")), [])

    def test_atomic_write_failure_cleans_temporary_file(self):
        self.output.write_text("previous")
        with patch.object(Path, "replace", side_effect=OSError("test failure")):
            with self.assertRaises(OSError):
                write_calls(self.output, [])
        self.assertEqual(self.output.read_text(), "previous")
        self.assertEqual(list(self.root.glob(".function-calls-*")), [])

    def test_vocabulary_display_characters_are_bytes(self):
        vocab = self.root / "vocab.json"
        vocab.write_text(json.dumps({"Ġhello": 0, "Ċ": 1, "Ã": 2, "©": 3}))
        pieces = vocabulary_bytes(vocab)
        self.assertEqual(pieces[0], b" hello")
        self.assertEqual(pieces[1], b"\n")
        self.assertEqual((pieces[2] + pieces[3]).decode(), "é")

    def test_exact_output_keys_and_types(self):
        function = Function.model_validate(self.function)
        for value in (1, 1.5, 10**100):
            call = Call(prompt="unchanged", name="anything", parameters={"value": value})
            validate_call(call, function)
            write_calls(self.output, [call])
            self.assertEqual(set(json.loads(self.output.read_text())[0]),
                             {"prompt", "name", "parameters"})
        for parameters in ({"value": True}, {"value": "1"}, {},
                           {"value": 1, "extra": 2}):
            with self.assertRaises(ValueError):
                validate_call(Call(prompt="x", name="anything",
                                   parameters=parameters), function)
        with self.assertRaises(ValidationError):
            Call(prompt="x", name="anything", parameters={"value": float("inf")})


if __name__ == "__main__":
    unittest.main()
