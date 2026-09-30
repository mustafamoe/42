"""Validate the flat function schema, prompt files and generated calls."""

import json
from pathlib import Path
from typing import Any, Literal, TypeAlias

from pydantic import BaseModel, ConfigDict, Field, TypeAdapter

Scalar: TypeAlias = str | int | float | bool | None
ScalarType: TypeAlias = Literal[
    "string", "number", "integer", "boolean", "null"
]


class Parameter(BaseModel):
    """Describe a mandatory scalar argument, without coercing its type."""

    model_config = ConfigDict(extra="forbid", strict=True)
    type: ScalarType
    description: str = ""


class ReturnType(BaseModel):
    """Describe the return type; functions are never executed."""

    model_config = ConfigDict(extra="forbid", strict=True)
    type: Literal[
        "string", "number", "integer", "boolean", "null", "array", "object"
    ]


class Function(BaseModel):
    """Validate one supplied function definition and its ordered arguments."""

    model_config = ConfigDict(extra="forbid", strict=True)
    name: str = Field(min_length=1)
    description: str
    parameters: dict[str, Parameter]
    returns: ReturnType


class Prompt(BaseModel):
    """Preserve an input request exactly, including empty strings."""

    model_config = ConfigDict(extra="forbid", strict=True)
    prompt: str


class Call(BaseModel):
    """Represent exactly the three required output keys."""

    model_config = ConfigDict(
        extra="forbid", strict=True, allow_inf_nan=False
    )
    prompt: str
    name: str
    parameters: dict[str, Scalar]


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    """Reject duplicate JSON keys instead of silently overwriting them."""
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key!r}")
        result[key] = value
    return result


def reject_constant(value: str) -> None:
    """Reject NaN and infinity, which are not JSON numbers."""
    raise ValueError(f"Invalid JSON constant: {value}")


def read_json(path: Path) -> Any:
    """Read strict UTF-8 JSON, reporting the path on any input failure."""
    try:
        with path.open(encoding="utf-8") as stream:
            return json.load(
                stream, object_pairs_hook=unique_object,
                parse_constant=reject_constant,
            )
    except (OSError, ValueError) as error:
        raise ValueError(f"Cannot read {path}: {error}") from error


def load_inputs(
    definitions_path: Path, prompts_path: Path,
) -> tuple[list[Function], list[Prompt]]:
    """Validate both files before expensive model loading begins."""
    functions = TypeAdapter(list[Function]).validate_python(
        read_json(definitions_path)
    )
    prompts = TypeAdapter(list[Prompt]).validate_python(
        read_json(prompts_path)
    )
    if not functions:
        raise ValueError("At least one function definition is required")
    if len({item.name for item in functions}) != len(functions):
        raise ValueError("Function names must be unique")
    return functions, prompts


def validate_call(call: Call, function: Function) -> None:
    """Verify exact keys and types, distinguishing booleans from numbers."""
    if call.name != function.name:
        raise ValueError("Generated function name does not match the schema")
    if call.parameters.keys() != function.parameters.keys():
        raise ValueError("Generated parameter keys do not match the schema")
    types: dict[str, tuple[type, ...]] = {
        "string": (str,), "number": (int, float), "integer": (int,),
        "boolean": (bool,), "null": (type(None),),
    }
    for name, parameter in function.parameters.items():
        if type(call.parameters[name]) not in types[parameter.type]:
            raise ValueError(f"Parameter {name!r} must be {parameter.type}")
