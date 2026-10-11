# inter

Level 3 · Python 3.10 · Submission file: `py_inter.py`

## Task

Return the characters that occur in both strings, including each character only once. Use the order of their first appearance in `s1`.

## Function signature

```python
def inter(s1: str, s2: str) -> str:
```

## Rules

- The comparison is case-sensitive.
- Spaces and punctuation count as characters.
- Return an empty string if there are no shared characters.

## Examples

| Call | Return value |
| --- | --- |
| `inter("mississippi", "simple")` | `"misp"` |
| `inter("abc", "xyz")` | `""` |
| `inter("", "abc")` | `""` |

Return the value from the function. The simulator imports the submission;
no command-line input or printed demonstration is required.
