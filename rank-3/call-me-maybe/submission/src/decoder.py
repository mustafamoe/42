"""Mask vocabulary logits using the chosen function's scalar JSON grammar."""

import json
import os
import re
from pathlib import Path
from typing import Any, Literal, cast

import numpy as np
from numpy.typing import NDArray
from pydantic import BaseModel, ConfigDict

from src.grammar import ScalarGrammar
from src.schema import (
    Call, Function, Scalar, number_as_float, read_json, validate_call,
)

MODEL_DIRECTORY = Path("model")
CONTEXT_LIMIT = 32768
VALUE_TOKEN_LIMIT = 256
COPY_LOGIT_BONUS = 3.5


def vocabulary_bytes(path: Path) -> dict[int, bytes]:
    """Undo Qwen's byte display map, preserving split UTF-8 tokens."""
    visible = (list(range(33, 127)) + list(range(161, 173))
               + list(range(174, 256)))
    byte_order = visible + [byte for byte in range(256) if byte not in visible]
    characters = visible + list(range(256, 256 + 256 - len(visible)))
    inverse = {chr(char): byte for char, byte in zip(characters, byte_order)}
    raw_vocab = read_json(path)
    if not isinstance(raw_vocab, dict) or not raw_vocab:
        raise ValueError("The SDK vocabulary must be a nonempty JSON object")
    result: dict[int, bytes] = {}
    for token, token_id in raw_vocab.items():
        if not isinstance(token, str) or type(token_id) is not int:
            raise ValueError("Invalid token or token ID in the SDK vocabulary")
        if token_id < 0 or token_id in result:
            raise ValueError("Vocabulary IDs must be unique and nonnegative")
        if token and all(char in inverse for char in token):
            result[token_id] = bytes(inverse[char] for char in token)
    if not result:
        raise ValueError("No byte tokens found in the SDK vocabulary")
    return result


def literal_source(text: str) -> tuple[bytes, frozenset[int]]:
    """Encode source characters separately to retain safe copy boundaries."""
    pieces = []
    boundaries = {0}
    length = 0
    for character in text:
        piece = json.dumps(character, ensure_ascii=False)[1:-1].encode("utf-8")
        pieces.append(piece)
        length += len(piece)
        boundaries.add(length)
    return b"".join(pieces), frozenset(boundaries)


class Decoder(BaseModel):
    """Generate scalar values through the public SDK and vocabulary."""

    model_config = ConfigDict(extra="forbid", strict=True)
    model: Any
    vocabulary: dict[int, bytes]

    def encode(self, text: str) -> list[int]:
        """Use the SDK tokenizer and its public tensor representation."""
        ids: list[int] = self.model.encode(text).tolist()[0]
        return ids

    def logits(self, ids: list[int]) -> NDArray[np.float64]:
        """Read a finite next-token logits vector through the public SDK."""
        if len(ids) >= CONTEXT_LIMIT:
            raise ValueError(
                f"Request exceeds the {CONTEXT_LIMIT}-token context"
            )
        logits = np.asarray(
            self.model.get_logits_from_input_ids(ids), dtype=np.float64
        )
        if logits.ndim != 1 or not logits.size:
            raise ValueError("The SDK returned an invalid logits vector")
        logits[~np.isfinite(logits)] = -np.inf
        return logits

    def select_token(
        self, ids: list[int], raw: bytes, grammar: ScalarGrammar,
        copy_pending: bool = False,
    ) -> int:
        """Mask invalid tokens, with a soft preference for literal copying."""
        logits = self.logits(ids)
        syntax = grammar.model_copy(update={
            "source": None, "boundaries": frozenset(),
        }) if grammar.source is not None else grammar
        ranked = np.argsort(-logits, kind="stable")
        token_id = -1
        for candidate_id in ranked:
            if not np.isfinite(logits[candidate_id]):
                break
            piece = self.vocabulary.get(int(candidate_id))
            if piece is not None and syntax.status(raw + piece) >= 0:
                token_id = int(candidate_id)
                break
        if token_id < 0:
            raise ValueError("No finite, schema-valid next token")
        if grammar.source is not None:
            if copy_pending:
                insensitive = grammar.model_copy(update={
                    "source": grammar.source.lower(),
                })
                candidate = (raw + self.vocabulary[token_id]).lower()
                if not insensitive.copy_at_boundary(candidate):
                    return token_id
            best_score = float(logits[token_id])
            for candidate_id in ranked:
                score = float(logits[candidate_id])
                if score + COPY_LOGIT_BONUS < best_score:
                    break
                piece = self.vocabulary.get(int(candidate_id))
                if piece is None or syntax.status(raw + piece) < 0:
                    continue
                if grammar.copy_at_boundary(raw + piece):
                    score += COPY_LOGIT_BONUS
                if (score > best_score or (
                    score == best_score and candidate_id < token_id
                )):
                    token_id = int(candidate_id)
                    best_score = score
        return token_id

    def generate(
        self, ids: list[int], grammar: ScalarGrammar, prefix: str = "",
    ) -> Scalar:
        """Mask invalid tokens, greedily decode, and return a JSON scalar.

        Args:
            ids: Model context, extended in place as tokens are selected.
            grammar: Required scalar type and terminating punctuation.
            prefix: Fixed JSON structure before the scalar.

        Returns:
            The decoded scalar, with the delimiter removed.

        Raises:
            ValueError: If no valid continuation exists or a limit is reached.
        """
        raw = b""
        remaining = VALUE_TOKEN_LIMIT
        unrestricted = grammar.model_copy(update={
            "source": None, "boundaries": frozenset(),
        })
        copy_pending = grammar.source is not None
        prefix_ids = self.encode(prefix) if prefix else []
        if grammar.kind == "string":
            first = self.select_token(
                ids + prefix_ids, raw, grammar, copy_pending,
            )
            piece = self.vocabulary[first]
            status = unrestricted.status(piece)
            if status == 1 or unrestricted.complete(piece.strip()):
                ids.extend(prefix_ids + [first])
                raw = piece
                remaining -= 1
                if status == 1:
                    return cast(Scalar, json.loads(raw[:-1]))
            else:
                ids.extend(self.encode(prefix + '"'))
                raw = b'"'
        else:
            ids.extend(prefix_ids)
        for step in range(remaining):
            matches = [choice for choice in grammar.choices
                       if choice.startswith(raw.lstrip())]
            if len(matches) == 1:
                suffix = matches[0][len(raw.lstrip()):]
                try:
                    completion = suffix.decode("utf-8")
                except UnicodeDecodeError:
                    pass
                else:
                    tokens = self.encode(completion)
                    if (len(tokens) <= remaining - step
                            and len(ids) + len(tokens) <= CONTEXT_LIMIT):
                        ids.extend(tokens)
                        return cast(Scalar, json.loads(matches[0][:-1]))
            token_id = self.select_token(
                ids, raw, grammar, copy_pending,
            )
            ids.append(token_id)
            raw += self.vocabulary[token_id]
            if grammar.source is not None and grammar.status(raw) < 0:
                grammar = unrestricted
                copy_pending = False
            if copy_pending and (
                unrestricted.status(raw) == 1
                or unrestricted.complete(raw)
                or grammar.copied_prefix(raw[1:], True)
            ):
                copy_pending = False
            if grammar.status(raw) == 1:
                return cast(Scalar, json.loads(raw[:-1]))
        raise ValueError(
            f"Generation exceeded {VALUE_TOKEN_LIMIT} tokens for one value"
        )

    def context(self, prompt: str, functions: list[Function]) -> str:
        """Build Qwen's tool template with its complete non-thinking prefix."""
        definitions = "\n".join(json.dumps({
            "type": "function",
            "function": {
                "name": item.name,
                "description": item.description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        key: value.model_dump(exclude_defaults=True)
                        for key, value in item.parameters.items()
                    },
                    "required": list(item.parameters),
                    "additionalProperties": False,
                },
            },
        }, ensure_ascii=True) for item in functions).replace("<", "\\u003c")
        text = (
            "<|im_start|>system\n"
            "Call exactly one tool, including the rejection tool when needed. "
            "Extract inputs; do not execute functions or compute results. "
            "Copy string content verbatim: preserve letter case, "
            "inner quotes, backslashes, newlines and braces. Omit only "
            "wrapping quotes or explicit boundary markers.\n\n"
            "# Tools\n\nYou may call one or more functions to assist "
            "with the user query.\n\n"
            "You are provided with function signatures within "
            "<tools></tools> XML tags:\n"
            f"<tools>\n{definitions}\n</tools>\n\n"
            "For each function call, return a json object with function "
            "name and arguments within <tool_call></tool_call> XML tags:\n"
            '<tool_call>\n{"name": <function-name>, '
            '"arguments": <args-json-object>}\n'
            "</tool_call><|im_end|>\n"
            f"<|im_start|>user\n{prompt}<|im_end|>\n"
            "<|im_start|>assistant\n<think>\n\n</think>\n\n"
        )
        return text

    def argument_request(self, prompt: str) -> str:
        """Identify text boundaries while protecting quoted literals."""
        unquoted = re.sub(
            r'"(?:[^"\\]|\\.)*"|(?<!\w)\'(?:[^\'\\]|\\.)*\'(?!\w)',
            lambda match: " " * len(match.group()), prompt,
        )
        introduction = re.search(
            r"\b(?:between\s+(?:the\s+)?markers|"
            r"(?:between|inside)\s+\S+\s+and\s+\S+)\s*[:.]",
            unquoted, flags=re.IGNORECASE,
        )
        if introduction is None:
            return prompt
        candidates = tuple(dict.fromkeys(re.findall(
            r"</?[^>\s]+>|\w+|[^\w\s]+", prompt,
        )))
        if not candidates:
            raise ValueError("No text boundary markers available")
        ids = self.encode(
            "<|im_start|>system\nIdentify explicitly designated text "
            "delimiter labels. Return opening_marker and closing_marker, "
            "not the instruction verb or message content. "
            "Answer a JSON object.<|im_end|>\n"
            f"<|im_start|>user\n{prompt}<|im_end|>\n"
            "<|im_start|>assistant\n<think>\n\n</think>\n\n{"
        )
        markers = []
        fields: tuple[tuple[str, Literal[",", "}"]], ...] = (
            ("opening_marker", ","), ("closing_marker", "}"),
        )
        for key, delimiter in fields:
            choices = tuple(
                (json.dumps(value, ensure_ascii=False) + delimiter).encode()
                for value in candidates
            )
            markers.append(cast(str, self.generate(
                ids, ScalarGrammar(
                    kind="string", delimiter=delimiter, choices=choices,
                ), json.dumps(key) + ":",
            )))
        opening, closing = markers
        end = prompt.rfind(closing)
        start = prompt.rfind(opening, 0, end)
        if start < 0 or end < start + len(opening):
            raise ValueError("Could not locate the selected text boundaries")
        content = prompt[start + len(opening):end]
        if opening[-1].isalnum() and content.startswith(" "):
            content = content[1:]
        if closing[0].isalnum() and content.endswith(" "):
            content = content[:-1]
        return (prompt[:introduction.start()].rstrip() + ":\n" + content
                + prompt[end + len(closing):])

    def call(self, prompt: str, functions: list[Function]) -> Call:
        """Choose a function using the model and decode its arguments.

        Args:
            prompt: Original request, preserved unchanged in the result.
            functions: Validated definitions with unique function names.

        Returns:
            A call containing every parameter of the selected function.
        """
        if not prompt.strip():
            raise ValueError("No available function matches this prompt")
        rejection_name = "no_matching_function"
        while any(item.name == rejection_name for item in functions):
            rejection_name = "_" + rejection_name
        rejection = Function.model_validate({
            "name": rejection_name,
            "description": (
                "Reject requests none of the other tools can fulfill, "
                "including unrelated questions, empty or unclear requests, "
                "and requests missing essential inputs."
            ),
            "parameters": {}, "returns": {"type": "null"},
        })
        available = functions + [rejection]
        ids = self.encode(self.context(prompt, available))
        ids.extend(self.encode("<tool_call>\n"))
        choices = tuple(
            json.dumps(item.name, ensure_ascii=False).encode("utf-8") + b","
            for item in available
        )
        name = self.generate(
            ids,
            ScalarGrammar(kind="string", delimiter=",", choices=choices),
            '{"name":',
        )
        if name == rejection_name:
            raise ValueError("No available function matches this prompt")
        function = next(item for item in functions if item.name == name)
        request = (self.argument_request(prompt) if any(
            item.type == "string" and item.enum is None
            for item in function.parameters.values()
        ) else prompt)
        if request != prompt:
            ids = self.encode(self.context(request, [function]))
            ids.extend(self.encode(
                '<tool_call>\n{"name":'
                + json.dumps(function.name).replace("<", "\\u003c")
                + ',"arguments":{'
            ))
        else:
            ids.extend(self.encode('"arguments":{'))
        parameters: dict[str, Scalar] = {}
        for index, (key, parameter) in enumerate(function.parameters.items()):
            delimiter: Literal[",", "}"] = (
                "," if index + 1 < len(function.parameters) else "}"
            )
            choices = (() if parameter.enum is None else tuple(
                json.dumps(value, ensure_ascii=False).encode("utf-8")
                + delimiter.encode() for value in parameter.enum
            ))
            source: bytes | None = None
            boundaries: frozenset[int] = frozenset()
            if parameter.type == "string" and parameter.enum is None:
                source, boundaries = literal_source(prompt)
            value = self.generate(
                ids,
                ScalarGrammar(
                    kind=parameter.type, delimiter=delimiter, choices=choices,
                    source=source, boundaries=boundaries,
                ),
                json.dumps(key) + ":",
            )
            if parameter.type == "number" and type(value) is int:
                value = number_as_float(value)
            parameters[key] = value
        result = Call(prompt=prompt, name=function.name, parameters=parameters)
        validate_call(result, function)
        return result


def load_decoder() -> Decoder:
    """Load the required model once, using only the supplied public SDK API."""
    MODEL_DIRECTORY.mkdir(parents=True, exist_ok=True)
    os.environ["HF_HUB_CACHE"] = str(MODEL_DIRECTORY.resolve())
    from llm_sdk import Small_LLM_Model

    model = Small_LLM_Model(trust_remote_code=False)
    vocabulary = vocabulary_bytes(Path(model.get_path_to_vocab_file()))
    return Decoder(model=model, vocabulary=vocabulary)
