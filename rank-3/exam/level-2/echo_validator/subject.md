# echo_validator

Level 2 · Python 3.10 · Submission file: `py_echo_validator.py`

## Task

Consider only the alphabetic characters of the input, without case. Return whether those characters read the same forwards and backwards.

## Function signature

```python
def echo_validator(text: str) -> bool:
```

## Rules

- Ignore spaces, digits, and punctuation.
- Return `False` if the input contains no letters.
- A single remaining letter is a palindrome.

## Examples

| Call | Return value |
| --- | --- |
| `echo_validator("No lemon, no melon!")` | `True` |
| `echo_validator("python")` | `False` |
| `echo_validator("123!")` | `False` |

Return the value from the function. The simulator imports the submission;
no command-line input or printed demonstration is required.
