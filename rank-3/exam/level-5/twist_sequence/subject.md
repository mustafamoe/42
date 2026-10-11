# twist_sequence

Level 5 · Python 3.10 · Submission file: `py_twist_sequence.py`

## Task

Rotate a list to the right by `k` positions, moving the final elements to the front while keeping their relative order.

## Function signature

```python
def twist_sequence(arr: list[int], k: int) -> list[int]:
```

## Rules

- `k` is a nonnegative integer and can be larger than the list length.
- Leave the input list unchanged.
- An empty list returns an empty list; rotating by zero keeps the order.

## Examples

| Call | Return value |
| --- | --- |
| `twist_sequence([10,20,30,40], 1)` | `[40,10,20,30]` |
| `twist_sequence([1,2,3], 5)` | `[2,3,1]` |
| `twist_sequence([], 3)` | `[]` |

Return the value from the function. The simulator imports the submission;
no command-line input or printed demonstration is required.
