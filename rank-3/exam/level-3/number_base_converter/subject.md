# number_base_converter

Level 3 · Python 3.10 · Submission file: `py_number_base_converter.py`

## Task

Convert a nonnegative integer represented as text from one base to another. Use `0` through `9` for the first ten values and `A` through `Z` for the rest.

## Function signature

```python
def number_base_converter(number: str, from_base: int, to_base: int) -> str:
```

## Rules

- Both bases must be integers between 2 and 36, inclusive.
- Accept ASCII letters in either case and return uppercase output.
- Return `"ERROR"` for an empty input, invalid digits, invalid bases, signs, whitespace, or non-ASCII characters.
- Represent zero as `"0"`, and remove redundant leading zeroes.

## Examples

| Call | Return value |
| --- | --- |
| `number_base_converter("1101", 2, 10)` | `"13"` |
| `number_base_converter("2a", 16, 2)` | `"101010"` |
| `number_base_converter("Z", 36, 10)` | `"35"` |

Return the value from the function. The simulator imports the submission;
no command-line input or printed demonstration is required.
