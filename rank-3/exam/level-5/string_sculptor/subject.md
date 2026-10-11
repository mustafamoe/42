# string_sculptor

Level 5 · Python 3.10 · Submission file: `py_string_sculptor.py`

## Task

Alternate the case of letters, starting with lowercase, then uppercase, and continuing in that pattern. Restart the pattern after each ordinary space.

## Function signature

```python
def string_sculptor(text: str) -> str:
```

## Rules

- Digits and punctuation stay unchanged and do not advance the letter index.
- Only the ASCII space character resets the pattern.
- Keep every nonalphabetic character in its original position.

## Examples

| Call | Return value |
| --- | --- |
| `string_sculptor("GOOD DAY")` | `"gOoD dAy"` |
| `string_sculptor("ab12cd")` | `"aB12cD"` |
| `string_sculptor("")` | `""` |

Return the value from the function. The simulator imports the submission;
no command-line input or printed demonstration is required.
