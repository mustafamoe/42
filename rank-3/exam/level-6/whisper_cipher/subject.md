# whisper_cipher

Level 6 · Python 3.10 · Submission file: `py_whisper_cipher.py`

## Task

Apply a Caesar cipher to English letters by moving each letter `shift` positions through the alphabet. Wrap around at either end.

## Function signature

```python
def whisper_cipher(text: str, shift: int) -> str:
```

## Rules

- Preserve uppercase and lowercase.
- Negative shifts move backwards; shifts may exceed 26.
- Keep digits, punctuation, spaces, and characters outside `A-Z` and `a-z` unchanged.

## Examples

| Call | Return value |
| --- | --- |
| `whisper_cipher("Zoo!", 2)` | `"Bqq!"` |
| `whisper_cipher("Abc", -1)` | `"Zab"` |
| `whisper_cipher("code", 26)` | `"code"` |

Return the value from the function. The simulator imports the submission;
no command-line input or printed demonstration is required.
