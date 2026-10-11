# hidenp

Level 3 · Python 3.10 · Submission file: `py_hidenp.py`

## Task

Return whether every character of `small` can be found in `big` in the same order. Matches do not need to be next to one another.

## Function signature

```python
def hidenp(small: str, big: str) -> bool:
```

## Rules

- The comparison is case-sensitive.
- Each character in `big` can match at most one character in `small`.
- An empty `small` is a subsequence of any string.

## Examples

| Call | Return value |
| --- | --- |
| `hidenp("cat", "c1a2t")` | `True` |
| `hidenp("cta", "cat")` | `False` |
| `hidenp("", "abc")` | `True` |

Return the value from the function. The simulator imports the submission;
no command-line input or printed demonstration is required.
