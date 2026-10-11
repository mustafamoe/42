"""Reverse the columns of every row without changing the input."""


def mirror_matrix(matrix: list[list[int]]) -> list[list[int]]:
    """Return a new matrix whose rows are individually reversed."""
    result: list[list[int]] = []
    for row in matrix:
        # Slicing makes a new row; it does not reverse the original in place.
        result.append(row[::-1])

    return result
