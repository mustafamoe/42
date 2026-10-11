# anagram

Level 4 · Python 3.10 · Submission file: `py_anagram.py`

## Task

Return whether the two strings contain the same characters with the same counts after ignoring case and ordinary spaces.

## Function signature

```python
def anagram(s1: str, s2: str) -> bool:
```

## Rules

- Ignore the ASCII space character `" "`; other whitespace is not removed.
- Every occurrence matters: two copies of a letter are different from one.
- Two empty strings are anagrams. Other characters remain part of the comparison.

## Examples

| Call | Return value |
| --- | --- |
| `anagram("rail safety", "Fairy tales")` | `True` |
| `anagram("hello", "world")` | `False` |
| `anagram("", "")` | `True` |

Return the value from the function. The simulator imports the submission;
no command-line input or printed demonstration is required.
