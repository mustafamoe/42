"""Mask vocabulary logits using the chosen function's scalar JSON grammar."""

import json
from pathlib import Path
from typing import Any, Literal, cast

import numpy as np
from pydantic import BaseModel, ConfigDict

from src.grammar import ScalarGrammar
from src.schema import Call, Function, Scalar, read_json, validate_call


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


class Decoder(BaseModel):
    """Generate scalar values through the public SDK and vocabulary."""

    model_config = ConfigDict(extra="forbid", strict=True)
    model: Any
    vocabulary: dict[int, bytes]

    def encode(self, text: str) -> list[int]:
        """Use the SDK tokenizer and its public tensor representation."""
        ids: list[int] = self.model.encode(text).tolist()[0]
        return ids

    def select_token(
        self, ids: list[int], raw: bytes, grammar: ScalarGrammar,
    ) -> int:
        """Mask invalid continuations and choose the highest finite logit."""
        if len(ids) >= 32768:
            raise ValueError("Request exceeds the 32768-token context")
        logits = np.asarray(
            self.model.get_logits_from_input_ids(ids), dtype=np.float64
        )
        if logits.ndim != 1 or not logits.size:
            raise ValueError("The SDK returned an invalid logits vector")
        masked = np.full(logits.shape, -np.inf)
        for token_id, piece in self.vocabulary.items():
            if token_id < logits.size and grammar.status(raw + piece) >= 0:
                masked[token_id] = logits[token_id]
        masked[~np.isfinite(masked)] = -np.inf
        token_id = int(np.argmax(masked))
        if not np.isfinite(masked[token_id]):
            raise ValueError("No finite, schema-valid next token")
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
        remaining = 256
        prefix_ids = self.encode(prefix) if prefix else []
        if grammar.kind == "string":
            first = self.select_token(ids + prefix_ids, raw, grammar)
            piece = self.vocabulary[first]
            status = grammar.status(piece)
            if status == 1 or grammar.complete(piece.strip()):
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
        for _ in range(remaining):
            token_id = self.select_token(ids, raw, grammar)
            ids.append(token_id)
            raw += self.vocabulary[token_id]
            if grammar.status(raw) == 1:
                return cast(Scalar, json.loads(raw[:-1]))
        raise ValueError("Generation exceeded 256 tokens for one value")

    def context(self, prompt: str, functions: list[Function]) -> str:
        """Build a request with the relevant function definitions."""
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
            "Choose exactly one function matching the user's request. "
            "Return its input arguments, without executing the function. "
            "Preserve string content and punctuation exactly, excluding "
            "surrounding quotes or boundary markers.\n\n"
            f"# Tools\n\n<tools>\n{definitions}\n</tools>\n\n"
            "Respond inside <tool_call> tags with a JSON object containing "
            "name and arguments.\n"
            '<tool_call>\n{"name": FUNCTION_NAME, "arguments": OBJECT}\n'
            "</tool_call><|im_end|>\n"
            f"<|im_start|>user\n{prompt}<|im_end|>\n"
            "<|im_start|>assistant\n<think>\n"
        )
        return text

    def reason(self, ids: list[int]) -> None:
        """Allow bounded internal analysis before constrained JSON decoding."""
        end = self.encode("</think>")
        eos = self.encode("<|im_end|>")
        for _ in range(56):
            if len(ids) >= 32700:
                raise ValueError("Request exceeds the model context")
            logits = np.asarray(
                self.model.get_logits_from_input_ids(ids), dtype=np.float64
            )
            if logits.ndim != 1 or not logits.size:
                raise ValueError("The SDK returned an invalid logits vector")
            logits[~np.isfinite(logits)] = -np.inf
            logits[eos] = -np.inf
            token_id = int(np.argmax(logits))
            if not np.isfinite(logits[token_id]):
                raise ValueError("No finite reasoning token available")
            ids.append(token_id)
            if ids[-len(end):] == end:
                break
        else:
            ids.extend(end)
        ids.extend(self.encode("\n\n<tool_call>\n"))

    def call(self, prompt: str, functions: list[Function]) -> Call:
        """Choose a function using the model and decode its arguments.

        Args:
            prompt: Original request, preserved unchanged in the result.
            functions: Validated definitions with unique function names.

        Returns:
            A call containing every parameter of the selected function.
        """
        ids = self.encode(self.context(prompt, functions))
        self.reason(ids)
        choices = tuple(
            json.dumps(item.name, ensure_ascii=False).encode("utf-8") + b","
            for item in functions
        )
        name = self.generate(
            ids,
            ScalarGrammar(kind="string", delimiter=",", choices=choices),
            '{"name":',
        )
        function = next(item for item in functions if item.name == name)
        ids.extend(self.encode('"arguments":{'))
        parameters: dict[str, Scalar] = {}
        for index, (key, parameter) in enumerate(function.parameters.items()):
            delimiter: Literal[",", "}"] = (
                "," if index + 1 < len(function.parameters) else "}"
            )
            parameters[key] = self.generate(
                ids,
                ScalarGrammar(kind=parameter.type, delimiter=delimiter),
                json.dumps(key) + ":",
            )
        result = Call(prompt=prompt, name=function.name, parameters=parameters)
        validate_call(result, function)
        return result


def load_decoder() -> Decoder:
    """Load the required model once, using only the supplied public SDK API."""
    from llm_sdk import Small_LLM_Model

    model = Small_LLM_Model(trust_remote_code=False)
    vocabulary = vocabulary_bytes(Path(model.get_path_to_vocab_file()))
    return Decoder(model=model, vocabulary=vocabulary)
