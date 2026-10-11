# pattern_tracker

Level 3 · Python 3.10 · Submission file: `py_pattern_tracker.py`

## Task

Count adjacent pairs of ASCII digits whose second digit is exactly one greater than the first.

## Function signature

```python
def pattern_tracker(text: str) -> int:
```

## Rules

- Pairs can overlap, so `"234"` contains two valid pairs.
- Characters between digits interrupt adjacency.
- The pair `"90"` does not wrap around and is not valid.

## Examples

| Call | Return value |
| --- | --- |
| `pattern_tracker("234")` | `2` |
| `pattern_tracker("23x45")` | `2` |
| `pattern_tracker("90")` | `0` |

Return the value from the function. The simulator imports the submission;
no command-line input or printed demonstration is required.
