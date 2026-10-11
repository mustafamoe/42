"""Load rank catalogs without importing any reference solution."""

import json
import keyword
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Exercise:
    """The information needed to assign and grade one exercise."""

    name: str
    level: int
    function: str
    filename: str
    subject: Path
    cases: tuple[dict[str, Any], ...]
    preserve_inputs: bool
    forbidden_names: tuple[str, ...]
    forbidden_attributes: tuple[str, ...]


@dataclass(frozen=True)
class Rank:
    """A complete exam profile and its exercise bank."""

    number: int
    title: str
    duration_seconds: int
    grading_timeout_seconds: int
    scores: tuple[int, ...]
    retry_delays_seconds: tuple[int, ...]
    exercises: tuple[Exercise, ...]

    @property
    def levels(self) -> tuple[int, ...]:
        return tuple(sorted({exercise.level for exercise in self.exercises}))


def integer(data: dict[str, Any], key: str, minimum: int = 1) -> int:
    value = data.get(key)
    if (
        not isinstance(value, int)
        or isinstance(value, bool)
        or value < minimum
    ):
        raise ValueError(f"{key} must be an integer >= {minimum}")
    return value


def text(data: dict[str, Any], key: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{key} must be a nonempty string")
    return value


def strings(data: dict[str, Any], key: str) -> tuple[str, ...]:
    values = data.get(key, [])
    if not isinstance(values, list) or any(
        not isinstance(value, str) for value in values
    ):
        raise ValueError(f"{key} must be a list of strings")
    return tuple(str(value) for value in values)


def integers(data: dict[str, Any], key: str) -> tuple[int, ...]:
    values = data.get(key)
    if not isinstance(values, list) or any(
        not isinstance(value, int) or isinstance(value, bool) or value < 0
        for value in values
    ):
        raise ValueError(f"{key} must be a list of nonnegative integers")
    return tuple(int(value) for value in values)


def load_exercise(data: Any, root: Path) -> Exercise:
    if not isinstance(data, dict):
        raise ValueError("each exercise must be an object")
    name = text(data, "name")
    function = text(data, "function")
    for identifier in (name, function):
        if not identifier.isidentifier() or keyword.iskeyword(identifier):
            raise ValueError(f"invalid identifier: {identifier}")

    filename = text(data, "filename")
    if (
        Path(filename).name != filename
        or "\\" in filename
        or not filename.endswith(".py")
    ):
        raise ValueError(f"invalid submission filename: {filename}")
    level = integer(data, "level")
    subject = root / f"level-{level}" / name / "subject.md"
    if not subject.is_file() or not subject.resolve().is_relative_to(root):
        raise ValueError(f"missing or misplaced subject for {name}")

    cases = data.get("cases")
    if not isinstance(cases, list) or not cases:
        raise ValueError(f"{name} needs at least one grading case")
    for case in cases:
        if (
            not isinstance(case, dict)
            or not isinstance(case.get("args"), list)
            or "expected" not in case
        ):
            raise ValueError(f"{name} has an invalid grading case")
    preserve_inputs = data.get("preserve_inputs", False)
    if not isinstance(preserve_inputs, bool):
        raise ValueError(f"{name}: preserve_inputs must be a boolean")

    return Exercise(
        name=name,
        level=level,
        function=function,
        filename=filename,
        subject=subject,
        cases=tuple(cases),
        preserve_inputs=preserve_inputs,
        forbidden_names=strings(data, "forbidden_names"),
        forbidden_attributes=strings(data, "forbidden_attributes"),
    )


def load_rank(path: Path) -> Rank:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("the rank catalog must be an object")
    number = integer(data, "rank")
    if path.parent.parent.name != f"rank-{number}":
        raise ValueError("rank number does not match its directory")
    entries = data.get("exercises")
    if not isinstance(entries, list) or not entries:
        raise ValueError("the rank catalog needs exercises")
    root = path.parent.resolve()
    exercises = tuple(load_exercise(entry, root) for entry in entries)
    if len({exercise.name for exercise in exercises}) != len(exercises):
        raise ValueError("exercise names must be unique within a rank")

    levels = tuple(sorted({exercise.level for exercise in exercises}))
    if levels != tuple(range(1, len(levels) + 1)):
        raise ValueError("levels must be consecutive, starting at 1")
    scores = integers(data, "scores")
    if (
        len(scores) != len(levels) + 1
        or scores[0] != 0
        or scores[-1] != 100
        or any(left >= right for left, right in zip(scores, scores[1:]))
    ):
        raise ValueError("scores must increase from 0 to 100, one per level")

    return Rank(
        number=number,
        title=text(data, "title"),
        duration_seconds=integer(data, "duration_seconds"),
        grading_timeout_seconds=integer(data, "grading_timeout_seconds"),
        scores=scores,
        retry_delays_seconds=integers(data, "retry_delays_seconds"),
        exercises=exercises,
    )
