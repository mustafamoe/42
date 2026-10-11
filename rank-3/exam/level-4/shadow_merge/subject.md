# shadow_merge

Level 4 · Python 3.10 · Submission file: `py_shadow_merge.py`

## Task

Combine two already sorted integer lists into a new ascending list containing every element from both inputs.

## Function signature

```python
def shadow_merge(list1: list[int], list2: list[int]) -> list[int]:
```

## Rules

- Both input lists are sorted in ascending order.
- Keep duplicate values and leave the inputs unchanged.
- Either or both input lists may be empty.

## Examples

| Call | Return value |
| --- | --- |
| `shadow_merge([0,4,8], [1,3,9])` | `[0,1,3,4,8,9]` |
| `shadow_merge([], [2,5])` | `[2,5]` |
| `shadow_merge([], [])` | `[]` |

Return the value from the function. The simulator imports the submission;
no command-line input or printed demonstration is required.
