"""Private regression for the string-opening token policy."""

import unittest
from unittest.mock import Mock

from src.decoder import Decoder
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
