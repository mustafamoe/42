"""Run private real-model regressions for the evaluation fixes."""

import json
import hashlib
import re
import signal
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "submission"))

from src.decoder import load_decoder
from src.schema import Function, read_json


def timeout(signum, frame):
    """Bound a diagnostic prompt without changing application behavior."""
    raise TimeoutError("Diagnostic prompt exceeded 90 seconds")


def main():
    root = Path(__file__).resolve().parent
    public = [Function.model_validate(item) for item in read_json(
        Path("data/input/functions_definition.json"),
    )]
    private = [Function.model_validate(item) for item in read_json(
        root / "moulinette/private/input/functions_definition.json",
    )]
    changed = [Function.model_validate(item) for item in read_json(
        root / "changed_functions.json",
    )]
    restricted = [Function.model_validate({
        "name": "open_document", "description": "Read a file with an encoding",
        "parameters": {
            "path": {"type": "string"},
            "encoding": {"type": "string", "enum": ["utf-8", "latin-1"]},
        },
        "returns": {"type": "string"},
    }), Function.model_validate({
        "name": "change_status", "description": "Set the task's status",
        "parameters": {
            "status": {"type": "string", "enum": ["queued", "active", "done"]},
        },
        "returns": {"type": "string"},
    })]
    notes = [Function.model_validate({
        "name": "archive_note", "description": "Archive a note verbatim",
        "parameters": {"body": {"type": "string"}},
        "returns": {"type": "null"},
    })]
    cases = [
        (public, "Which planet is closest to the Sun?", None, None),
        (public, "", None, None),
        (public, "Please help me with it.", None, None),
        (private, 'Format template: Say "hello" to {name}',
         "fn_format_template", {"template": 'Say "hello" to {name}'}),
        (private, 'Format template: Please say "welcome" to {visitor}',
         "fn_format_template", {"template": 'Please say "welcome" to {visitor}'}),
        (changed, "Save this exact message between markers. BEGIN path C:\\temp END",
         "save_message", {"text": "path C:\\temp"}),
        (changed, "Save this exact message between markers. BEGIN first line\nsecond line END",
         "save_message", {"text": "first line\nsecond line"}),
        (restricted, "Read /tmp/report.txt using latin-1 encoding.",
         "open_document", {"path": "/tmp/report.txt", "encoding": "latin-1"}),
        (restricted, "Set the task status to done.",
         "change_status", {"status": "done"}),
        (public, "Replace cat followed by one or more digits in 'cat12 dog cat cat7' with TOKEN.",
         "fn_substitute_string_with_regex", {
             "source_string": "cat12 dog cat cat7", "replacement": "TOKEN",
             "result": "TOKEN dog cat TOKEN",
         }),
        (public, "Greet shrek", "fn_greet", {"name": "shrek"}),
        (public, 'Replace all numbers in "Hello 34 I\'m 233 years old" with NUMBERS',
         "fn_substitute_string_with_regex", {
             "source_string": "Hello 34 I'm 233 years old", "replacement": "NUMBERS",
             "result": "Hello NUMBERS I'm NUMBERS years old",
         }),
        (notes, 'Archive the text between START and STOP: START café "hello" STOP',
         "archive_note", {"body": 'café "hello"'}),
        (notes, 'Archive only the text inside <note> and </note>: <note>first\nsecond</note>',
         "archive_note", {"body": 'first\nsecond'}),
        (changed, 'Save the literal message "BEGIN path END".',
         "save_message", {"text": 'BEGIN path END'}),
        (notes, 'Archive the literal note "START here STOP".',
         "archive_note", {"body": 'START here STOP'}),
        (notes, 'Archive the text between << and >>: <<Use BEGIN and END literally>>',
         "archive_note", {"body": 'Use BEGIN and END literally'}),
    ]
    started = time.monotonic()
    hashes = {
        path.name: hashlib.sha256(path.read_bytes()).hexdigest()
        for path in (root.parent / "submission/src").glob("*.py")
    }
    decoder = load_decoder()
    load_seconds = time.monotonic() - started
    results = []
    signal.signal(signal.SIGALRM, timeout)
    start = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    stop = int(sys.argv[2]) if len(sys.argv) > 2 else len(cases)
    output = (Path(sys.argv[3]) if len(sys.argv) > 3 else
              root / "moulinette/completion_probes.json")
    for functions, prompt, name, parameters in cases[start:stop]:
        started = time.monotonic()
        signal.alarm(90)
        record = {"prompt": prompt, "expected_name": name,
                  "expected_parameters": parameters}
        try:
            call = decoder.call(prompt, functions)
            record["actual"] = call.model_dump()
            if parameters is not None and "result" in parameters:
                record["passed"] = (call.name == name and all(
                    call.parameters[key] == parameters[key]
                    for key in ("source_string", "replacement")
                ) and re.sub(
                    call.parameters["regex"], call.parameters["replacement"],
                    call.parameters["source_string"],
                ) == parameters["result"])
            else:
                record["passed"] = call.name == name and call.parameters == parameters
        except Exception as error:
            record["error"] = str(error)
            record["passed"] = (name is None and isinstance(error, ValueError)
                                and "No available function matches" in str(error))
        finally:
            signal.alarm(0)
        record["seconds"] = round(time.monotonic() - started, 3)
        results.append(record)
        print(json.dumps(record, ensure_ascii=False), flush=True)
        output.write_text(json.dumps({
            "source_sha256": hashes,
            "model_load_seconds": round(load_seconds, 3), "results": results,
        }, ensure_ascii=True, indent=2) + "\n")
    passed = sum(item["passed"] for item in results)
    print(f"Evaluation regressions: {passed}/{len(results)}", flush=True)
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
