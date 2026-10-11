# cryptic_sorter

Level 1 · Python 3.10 · Submission file: `py_cryptic_sorter.py`

## Task

Return the strings ordered by three ascending keys: length first, text second with English letters compared without case, then the number of vowels. If all keys match, keep their input order.

## Function signature

```python
def cryptic_sorter(strings: list[str]) -> list[str]:
```

## Rules

- Inputs use ASCII characters; preserve the original spelling of each string.
- Vowels are `a`, `e`, `i`, `o`, and `u`, in either case.
- Do not use `sorted()` or `list.sort()`. Leave the input list unchanged.

## Examples

| Call | Return value |
| --- | --- |
| `cryptic_sorter(["plum","Fig","pear","a"])` | `["a","Fig","pear","plum"]` |
| `cryptic_sorter(["bb","AA","aa","BB"])` | `["AA","aa","bb","BB"]` |
| `cryptic_sorter([])` | `[]` |

Return the value from the function. The simulator imports the submission;
no command-line input or printed demonstration is required.
