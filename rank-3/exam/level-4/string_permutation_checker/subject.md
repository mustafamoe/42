# string_permutation_checker

Level 4 · Python 3.10 · Submission file: `py_string_permutation_checker.py`

## Task

Return whether one string can be rearranged to produce the other without adding, removing, or changing any character.

## Function signature

```python
def string_permutation_checker(s1: str, s2: str) -> bool:
```

## Rules

- The comparison is case-sensitive.
- Spaces, tabs, and punctuation count like any other character.
- Character counts must match exactly; two empty strings are permutations.

## Examples

| Call | Return value |
| --- | --- |
| `string_permutation_checker("a! b", "b !a")` | `True` |
| `string_permutation_checker("Abc", "abc")` | `False` |
| `string_permutation_checker("", "")` | `True` |

Return the value from the function. The simulator imports the submission;
no command-line input or printed demonstration is required.
