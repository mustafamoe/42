"""Grade a Python function in a fresh process with a bounded runtime."""

import ast
import copy
import importlib.util
import json
import os
import signal
import subprocess
import sys
import tempfile
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Grade:
    """A verdict suitable for the shell and its grading trace."""

    passed: bool
    message: str


def equal(actual: Any, expected: Any) -> bool:
    """Compare values and types, so True cannot stand in for integer 1."""
    if type(actual) is not type(expected):
        return False
    if isinstance(expected, list):
        return len(actual) == len(expected) and all(
            equal(left, right) for left, right in zip(actual, expected)
        )
    if isinstance(expected, dict):
        return actual.keys() == expected.keys() and all(
            equal(actual[key], value) for key, value in expected.items()
        )
    return bool(actual == expected)


def check_source(
    source: str,
    forbidden_names: tuple[str, ...],
    forbidden_attributes: tuple[str, ...],
) -> Grade | None:
    try:
        tree = ast.parse(source)
    except SyntaxError as error:
        return Grade(False, f"Syntax error on line {error.lineno}.")
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and node.id in forbidden_names:
            return Grade(False, f"Forbidden reference: {node.id}.")
        if (
            isinstance(node, ast.Attribute)
            and node.attr in forbidden_attributes
        ):
            return Grade(False, f"Forbidden method reference: .{node.attr}.")
    return None


def evaluate(
    submission: Path,
    function_name: str,
    cases: list[dict[str, Any]],
    preserve_inputs: bool,
) -> Grade:
    """Called only in the worker process, never in the interactive shell."""
    spec = importlib.util.spec_from_file_location("submission", submission)
    if spec is None or spec.loader is None:
        return Grade(False, "Could not load the submission.")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    try:
        spec.loader.exec_module(module)
    except BaseException as error:
        return Grade(False, f"Import raised {type(error).__name__}.")
    function = getattr(module, function_name, None)
    if not callable(function):
        return Grade(False, f"Missing callable function: {function_name}.")

    for index, case in enumerate(cases, start=1):
        args = copy.deepcopy(case["args"])
        original = copy.deepcopy(args)
        try:
            actual = function(*args)
            if preserve_inputs and not equal(args, original):
                return Grade(False, f"Case {index}: input was modified.")
            if not equal(actual, case["expected"]):
                return Grade(False, f"Case {index}: incorrect return value.")
        except BaseException as error:
            return Grade(False, f"Case {index} raised {type(error).__name__}.")
    return Grade(True, "All grading cases passed.")


def stop_process(process: subprocess.Popen[bytes]) -> None:
    """Also stop any descendants left in the worker's process group."""
    try:
        os.killpg(process.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    process.wait()


def grade(
    submission: Path,
    function_name: str,
    cases: tuple[dict[str, Any], ...],
    timeout: float,
    preserve_inputs: bool = False,
    forbidden_names: tuple[str, ...] = (),
    forbidden_attributes: tuple[str, ...] = (),
) -> Grade:
    if submission.is_symlink() or not submission.is_file():
        return Grade(False, "The required submission must be a regular file.")
    try:
        source = submission.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return Grade(False, "Could not read the submission as UTF-8.")
    rejected = check_source(source, forbidden_names, forbidden_attributes)
    if rejected is not None:
        return rejected
    if timeout <= 0:
        return Grade(False, "The exam deadline has expired.")

    with tempfile.TemporaryDirectory(prefix="examshell-grade-") as directory:
        root = Path(directory)
        # Grade this snapshot even if the student edits their file mid-run.
        snapshot = root / "submission.py"
        snapshot.write_text(source, encoding="utf-8")
        request = root / "request.json"
        request.write_text(json.dumps({
            "function": function_name,
            "cases": cases,
            "preserve_inputs": preserve_inputs,
        }), encoding="utf-8")
        result = root / "result.json"
        process = subprocess.Popen(
            [sys.executable, "-I", "-B", str(Path(__file__).resolve()),
             "--worker", str(snapshot), str(request), str(result)],
            cwd=root,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )
        try:
            process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            stop_process(process)
            return Grade(False, f"Grading exceeded {timeout:.1f} seconds.")
        except BaseException:
            stop_process(process)
            raise
        else:
            # A finished submission can still have spawned a child process.
            stop_process(process)

        if process.returncode != 0:
            return Grade(False, "The evaluation process exited unexpectedly.")
        try:
            verdict = json.loads(result.read_text(encoding="utf-8"))
            if (
                not isinstance(verdict, dict)
                or not isinstance(verdict.get("passed"), bool)
                or not isinstance(verdict.get("message"), str)
            ):
                raise ValueError("invalid worker verdict")
            return Grade(verdict["passed"], verdict["message"])
        except (OSError, UnicodeError, ValueError):
            return Grade(False, "The evaluation process returned no verdict.")


def worker() -> None:
    submission, request, result = map(Path, sys.argv[2:])
    data = json.loads(request.read_text(encoding="utf-8"))
    verdict = evaluate(
        submission, data["function"], data["cases"], data["preserve_inputs"],
    )
    result.write_text(json.dumps(asdict(verdict)), encoding="utf-8")


if __name__ == "__main__":
    if len(sys.argv) == 5 and sys.argv[1] == "--worker":
        worker()
    else:
        print("Start the shell with: python3.10 examshell/examshell.py")
