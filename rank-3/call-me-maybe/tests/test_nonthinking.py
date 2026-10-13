"""Guard the non-thinking prompt and inference call count without a model."""

import unittest
from unittest.mock import Mock

import numpy as np

from src.decoder import Decoder
from src.schema import Function


class NonThinkingTests(unittest.TestCase):
    def setUp(self):
        self.function = Function.model_validate({
            "name": "record", "description": "Record a measurement",
            "parameters": {"reading": {"type": "integer"}},
            "returns": {"type": "null"},
        })

    def test_only_function_and_value_selection_require_inference(self):
        sdk = Mock()
        encoded = []
        contexts = []
        scores = iter(([9, 0], [0, 9]))

        def encode(text):
            encoded.append(text)
            return np.asarray([[100 + len(encoded)]])

        def logits(ids):
            contexts.append(ids.copy())
            return next(scores)

        sdk.encode.side_effect = encode
        sdk.get_logits_from_input_ids.side_effect = logits
        decoder = Decoder(model=sdk, vocabulary={0: b'"record",', 1: b'3}'})
        call = decoder.call("Record the reading 3.", [self.function])
        self.assertEqual(call.parameters, {"reading": 3})
        self.assertEqual(call.name, "record")
        self.assertEqual(len(contexts), 2)
        self.assertTrue(all(101 in ids for ids in contexts))
        self.assertTrue(encoded[0].endswith(
            "<|im_start|>assistant\n<think>\n\n</think>\n\n",
        ))
        self.assertEqual(encoded[1], "<tool_call>\n")

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
