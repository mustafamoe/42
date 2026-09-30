"""Recognize JSON scalar prefixes at byte boundaries inside BPE tokens."""

import json
import math
import re
from typing import Literal

from pydantic import BaseModel, ConfigDict

from src.schema import ScalarType

STRING_BODY = rb'(?:[^"\\\x00-\x1f]|\\["\\/bfnrt]|\\u[0-9a-fA-F]{4})*'
STRING_PREFIX = re.compile(
    rb'"' + STRING_BODY + rb'(?:\\(?:u[0-9a-fA-F]{0,3})?)?'
)
STRING_COMPLETE = re.compile(rb'"' + STRING_BODY + rb'"')
INTEGER = rb'-?(?:0|[1-9][0-9]*)'
MANTISSA = INTEGER + rb'(?:\.[0-9]+)?'
NUMBER_COMPLETE = re.compile(MANTISSA + rb'(?:[eE][+-]?[0-9]+)?')
NUMBER_PREFIX = re.compile(
    rb'(?:|-|' + INTEGER + rb'(?:\.[0-9]*)?|'
    + MANTISSA + rb'[eE][+-]?[0-9]*)'
)
INTEGER_PREFIX = re.compile(rb'(?:|-|' + INTEGER + rb')')
INTEGER_COMPLETE = re.compile(INTEGER)


def valid_utf8_prefix(raw: bytes) -> bool:
    """Accept complete UTF-8 or an unfinished final character."""
    try:
        raw.decode("utf-8")
        return True
    except UnicodeDecodeError as error:
        return error.reason == "unexpected end of data"


class ScalarGrammar(BaseModel):
    """Accept only prefixes of a typed JSON value and its fixed delimiter."""

    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)
    kind: ScalarType
    delimiter: Literal[",", "}"]
    choices: tuple[bytes, ...] = ()

    def status(self, raw: bytes) -> int:
        """Return -1 for invalid, 0 for unfinished, or 1 for complete bytes."""
        raw = raw.lstrip(b" \t\r\n")
        if self.choices:
            if raw in self.choices:
                return 1
            valid = any(item.startswith(raw) for item in self.choices)
            return 0 if valid else -1
        if self.kind in ("boolean", "null"):
            values = ((b"true", b"false") if self.kind == "boolean"
                      else (b"null",))
            options = [value + self.delimiter.encode() for value in values]
            if raw in options:
                return 1
            return 0 if any(item.startswith(raw) for item in options) else -1
        if raw.endswith(self.delimiter.encode()):
            value = raw[:-1].rstrip(b" \t\r\n")
            if self.complete(value):
                return 1
        if self.kind == "string":
            if not valid_utf8_prefix(raw):
                return -1
            if not raw or STRING_PREFIX.fullmatch(raw):
                return 0
            return 0 if self.complete(raw.rstrip(b" \t\r\n")) else -1
        prefix = INTEGER_PREFIX if self.kind == "integer" else NUMBER_PREFIX
        if prefix.fullmatch(raw):
            return 0
        return 0 if self.complete(raw.rstrip(b" \t\r\n")) else -1

    def complete(self, raw: bytes) -> bool:
        """Check that a scalar is fully formed and finite before closure."""
        if self.kind == "string":
            return (bool(STRING_COMPLETE.fullmatch(raw))
                    and valid_utf8_prefix(raw))
        pattern = (INTEGER_COMPLETE if self.kind == "integer"
                   else NUMBER_COMPLETE)
        if not pattern.fullmatch(raw):
            return False
        value = json.loads(raw)
        return not isinstance(value, float) or math.isfinite(value)
