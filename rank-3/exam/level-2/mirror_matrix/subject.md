# mirror_matrix

Level 2 · Python 3.10 · Submission file: `py_mirror_matrix.py`

## Task

Return a new matrix with the elements of each row in reverse order. Keep the rows themselves in their original order.

## Function signature

```python
def mirror_matrix(matrix: list[list[int]]) -> list[list[int]]:
```

## Rules

- Leave the input matrix unchanged.
- Handle empty matrices and empty rows.
- Rows may have different lengths.

## Examples

| Call | Return value |
| --- | --- |
| `mirror_matrix([[2,4,6],[1,3]])` | `[[6,4,2],[3,1]]` |
| `mirror_matrix([])` | `[]` |
| `mirror_matrix([[]])` | `[[]]` |

Return the value from the function. The simulator imports the submission;
no command-line input or printed demonstration is required.
