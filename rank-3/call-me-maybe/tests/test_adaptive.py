"""Check model-controlled reasoning without altering constrained outputs."""

import unittest
from unittest.mock import Mock, patch

import numpy as np

from src.decoder import (
    Decoder, LITERAL_REASONING_TOKEN_LIMIT, REASONING_TOKEN_LIMIT,
)
from src.schema import Function


class AdaptiveTests(unittest.TestCase):
    """Keep the analysis decision separate from function and value selection."""

    def setUp(self):
        self.function = Function.model_validate({
            "name": "record", "description": "Record a measurement",
            "parameters": {"reading": {"type": "integer"}},
            "returns": {"type": "null"},
        })

    def test_budget_boolean_masks_invalid_tokens_and_follows_model_choice(self):
        for scores, expected in (
            ([100, 3, 2], 0), ([100, 2, 3], REASONING_TOKEN_LIMIT),
        ):
            with self.subTest(expected=expected):
                sdk = Mock()
                sdk.encode.return_value.tolist.return_value = [[42]]
                sdk.get_logits_from_input_ids.return_value = scores
                decoder = Decoder(model=sdk, vocabulary={
                    0: b'"guess"}', 1: b'false}', 2: b'true}',
                })
                self.assertEqual(decoder.reasoning_budget(
                    "Record the reading 3.", [self.function],
                ), expected)
                context = sdk.encode.call_args_list[0].args[0]
                self.assertIn(self.function.name, context)
                self.assertIn(self.function.description, context)
                self.assertIn("Record the reading 3.", context)
                sdk.get_logits_from_input_ids.assert_called_once()

    def test_copy_request_skips_reasoning_and_keeps_analysis_out_of_context(self):
        sdk = Mock()
        encoded = []
        contexts = []
        scores = iter(([9, 0, 0], [0, 9, 0], [0, 0, 9]))

        def encode(text):
            encoded.append(text)
            return np.asarray([[100 + len(encoded)]])

        def logits(ids):
            contexts.append(ids.copy())
            return next(scores)

        sdk.encode.side_effect = encode
        sdk.get_logits_from_input_ids.side_effect = logits
        decoder = Decoder(model=sdk, vocabulary={
            0: b'false}', 1: b'"record",', 2: b'3}',
        })
        call = decoder.call("Record the reading 3.", [self.function])
        self.assertEqual(call.name, "record")
        self.assertEqual(call.parameters, {"reading": 3})
        self.assertEqual(len(contexts), 3)
        analysis_token = next(101 + i for i, text in enumerate(encoded)
                              if "Answer a JSON object with needs_analysis" in text)
        self.assertIn(analysis_token, contexts[0])
        self.assertTrue(all(analysis_token not in ids for ids in contexts[1:]))
        self.assertTrue(all(101 in ids for ids in contexts[1:]))

    def test_literal_text_keeps_analysis_when_the_model_says_copy(self):
        sdk = Mock()
        sdk.encode.return_value.tolist.return_value = [[42]]
        sdk.get_logits_from_input_ids.return_value = [9, 0]
        decoder = Decoder(model=sdk, vocabulary={0: b'false}', 1: b'true}'})
        for prompt in (
            'Save the message \'She said "hello".\'',
            "Keep a\\b", "Keep first\nsecond", "Keep {name}",
        ):
            with self.subTest(prompt=prompt):
                self.assertEqual(decoder.reasoning_budget(
                    prompt, [self.function],
                ), LITERAL_REASONING_TOKEN_LIMIT)

    def test_request_needing_analysis_keeps_full_reasoning_budget(self):
        sdk = Mock()
        sdk.encode.return_value.tolist.return_value = [[42]]
        decoder = Decoder(model=sdk, vocabulary={0: b'3}'})
        with patch.object(Decoder, "reasoning_budget", return_value=48), \
                patch.object(Decoder, "reason") as reason, \
                patch.object(Decoder, "generate", side_effect=["record", 3]):
            decoder.call("Record the reading 3.", [self.function])
        self.assertEqual(reason.call_args.kwargs["budget"], REASONING_TOKEN_LIMIT)

    def test_blank_requests_fail_before_model_work(self):
        sdk = Mock()
        decoder = Decoder(model=sdk, vocabulary={0: b'3}'})
        for prompt in ("", " \t\r\n"):
            with self.subTest(prompt=prompt), self.assertRaisesRegex(
                ValueError, "No available function matches",
            ):
                decoder.call(prompt, [self.function])
        sdk.encode.assert_not_called()
        sdk.get_logits_from_input_ids.assert_not_called()
