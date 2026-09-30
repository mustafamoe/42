"""Score real-model output against independent expected calls, without inference."""

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "submission"))

from src.schema import Call, load_inputs, validate_call


def main():
    root = Path(__file__).resolve().parent
    mode = sys.argv[2] if len(sys.argv) > 2 else "supplied"
    if mode == "edge":
        definitions = root / "changed_functions.json"
        prompts_path = root / "edge_prompts.json"
        expected = [
            (None, None),
            (None, None),
            ("save_message", {"text": "path C:\\temp"}),
            ("save_message", {"text": "first line\nsecond line"}),
        ]
    elif mode == "changed":
        definitions = root / "changed_functions.json"
        prompts_path = root / "changed_prompts.json"
        expected = [
            ("multiply_values", {"left": 7, "right": 9}),
            ("multiply_values", {"left": -2.5, "right": 4}),
            ("multiply_values", {"left": 1234567890123, "right": 2}),
            ("save_message", {"text": ""}),
            ("save_message", {"text": "café مرحبا 😀"}),
            ("save_message", {"text": 'She said "hello".'}),
            ("set_reminder", {"task": "water plants", "days": 3, "notify": True}),
            ("set_reminder", {"task": "read", "days": 0, "notify": False}),
            ("clear_setting", {"value": None}),
            ("check_status", {}),
        ]
    else:
        definitions = Path("data/input/functions_definition.json")
        prompts_path = Path("data/input/function_calling_tests.json")
        expected = [
            ("fn_add_numbers", {"a": 2, "b": 3}),
            ("fn_add_numbers", {"a": 265, "b": 345}),
            ("fn_greet", {"name": "shrek"}),
            ("fn_greet", {"name": "john"}),
            ("fn_reverse_string", {"s": "hello"}),
            ("fn_reverse_string", {"s": "world"}),
            ("fn_get_square_root", {"a": 16}),
            ("fn_get_square_root", {"a": 144}),
            ("fn_substitute_string_with_regex", {
                "source_string": "Hello 34 I'm 233 years old",
                "replacement": "NUMBERS", "result": "Hello NUMBERS I'm NUMBERS years old",
            }),
            ("fn_substitute_string_with_regex", {
                "source_string": "Programming is fun", "replacement": "*",
                "result": "Pr*gr*mm*ng *s f*n",
            }),
            ("fn_substitute_string_with_regex", {
                "source_string": "The cat sat on the mat with another cat",
                "replacement": "dog", "result": "The dog sat on the mat with another dog",
            }),
        ]
    functions, prompts = load_inputs(definitions, prompts_path)
    available = {item.name: item for item in functions}
    data = json.loads(Path(sys.argv[1]).read_text())
    assert len(data) == len(prompts) == len(expected)
    correct = 0
    scored = 0
    for index, (raw, prompt, (name, parameters)) in enumerate(zip(data, prompts, expected), 1):
        call = Call.model_validate(raw)
        validate_call(call, available[call.name])
        assert call.prompt == prompt.prompt
        if name is None:
            print(f"SCHEMA ONLY {index}: ambiguous request {prompt.prompt!r}")
            continue
        scored += 1
        matches = call.name == name
        if "result" in parameters:
            matches = matches and all(
                call.parameters[key] == parameters[key]
                for key in ("source_string", "replacement")
            )
            if matches:
                try:
                    result = re.sub(call.parameters["regex"], call.parameters["replacement"],
                                    call.parameters["source_string"])
                    matches = result == parameters["result"]
                except re.error:
                    matches = False
        else:
            matches = matches and call.parameters == parameters
        correct += matches
        print(f"{'PASS' if matches else 'FAIL'} {index}: {prompt.prompt}")
        if not matches:
            print(f"  Actual: {call.model_dump()}")
    print(f"Schema: {len(data)}/{len(data)}; semantic accuracy: {correct}/{scored} "
          f"({100 * correct / scored:.1f}%)")
    return 0 if correct / scored >= 0.9 else 1


if __name__ == "__main__":
    sys.exit(main())
