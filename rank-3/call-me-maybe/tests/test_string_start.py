"""Private regression for the string-opening token policy."""

import unittest
from unittest.mock import Mock

import numpy as np

from src.decoder import CONTEXT_LIMIT, Decoder
from src.grammar import ScalarGrammar


class StringStartTests(unittest.TestCase):
    """Preserve whole literals while conditioning partial content on a quote."""

    def test_partial_content_waits_for_opening_quote(self):
        sdk = Mock()
        sdk.encode.return_value.tolist.return_value = [[42]]
        sdk.get_logits_from_input_ids.side_effect = [
            [100, 3, -1], [100, -1, 3],
        ]
        decoder = Decoder(
            model=sdk, vocabulary={0: b'"wrong', 1: b'"', 2: b'right"}'},
        )
        value = decoder.generate(
            [42], ScalarGrammar(kind="string", delimiter="}"),
        )
        self.assertEqual(value, "right")

    def test_finite_choice_waits_for_model_disambiguation(self):
        sdk = Mock()
        sdk.encode.side_effect = lambda text: np.asarray([
            {'"': [42], ',': [43]}[text],
        ])
        sdk.get_logits_from_input_ids.side_effect = [
            [10, 0, 0], [0, 10, 0], [0, 0, 10],
        ]
        decoder = Decoder(model=sdk, vocabulary={
            0: b'"fo', 1: b'fo', 2: b'obar"',
        })
        ids = []
        value = decoder.generate(ids, ScalarGrammar(
            kind="string", delimiter=",", choices=(b'"foo",', b'"foobar",'),
        ))
        self.assertEqual(value, "foobar")
        self.assertEqual(ids, [42, 1, 2, 43])
        self.assertEqual(sdk.get_logits_from_input_ids.call_count, 3)

    def test_finite_choice_preserves_split_utf8_before_completion(self):
        sdk = Mock()
        sdk.encode.side_effect = lambda text: np.asarray([
            {'"': [42], 'one",': [43]}[text],
        ])
        sdk.get_logits_from_input_ids.side_effect = [
            [10, 0, 0], [0, 10, 0], [0, 0, 10],
        ]
        decoder = Decoder(model=sdk, vocabulary={
            0: b'"\xc3', 1: b'\xc3', 2: b'\xa9',
        })
        ids = []
        value = decoder.generate(ids, ScalarGrammar(
            kind="string", delimiter=",",
            choices=('"éone",'.encode(), b'"Etwo",'),
        ))
        self.assertEqual(value, "éone")
        self.assertEqual(ids, [42, 1, 2, 43])
        self.assertEqual(sdk.get_logits_from_input_ids.call_count, 3)

    def test_finite_choice_respects_value_token_limit(self):
        sdk = Mock()
        sdk.encode.side_effect = lambda text: np.asarray([list(range(len(text)))])
        sdk.get_logits_from_input_ids.return_value = [10]
        decoder = Decoder(model=sdk, vocabulary={0: b'1'})
        with self.assertRaisesRegex(ValueError, "256"):
            decoder.generate([], ScalarGrammar(
                kind="integer", delimiter=",", choices=(b'1' * 257 + b',',),
            ))
        self.assertEqual(sdk.get_logits_from_input_ids.call_count, 256)

    def test_finite_choice_cannot_bypass_context_limit(self):
        sdk = Mock()
        sdk.encode.return_value.tolist.return_value = [[0]]
        decoder = Decoder(model=sdk, vocabulary={0: b'1,'})
        with self.assertRaisesRegex(ValueError, "context"):
            decoder.generate([0] * CONTEXT_LIMIT, ScalarGrammar(
                kind="integer", delimiter=",", choices=(b'1,',),
            ))
        sdk.get_logits_from_input_ids.assert_not_called()
