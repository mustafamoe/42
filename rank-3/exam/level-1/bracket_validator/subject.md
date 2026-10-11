# bracket_validator

Level 1 · Python 3.10 · Submission file: `py_bracket_validator.py`

## Task

Decide whether all brackets in a string are correctly matched and nested. Each closing bracket must match the most recent opening bracket that has not been closed.

## Function signature

```python
def bracket_validator(s: str) -> bool:
```

## Rules

- Handle `()`, `[]`, and `{}`.
- Ignore characters that are not brackets.
- Return `True` for an empty string; return `False` if any bracket is unmatched.

## Examples

| Call | Return value |
| --- | --- |
| `bracket_validator("[a{b(c)}]")` | `True` |
| `bracket_validator("([)]")` | `False` |
| `bracket_validator("")` | `True` |

Return the value from the function. The simulator imports the submission;
no command-line input or printed demonstration is required.
