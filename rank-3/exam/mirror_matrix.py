
def mirror_matrix(matrix: list[list[int]]) -> list[list[int]]:
    result: list[list[int]] = []

    for row in matrix:
        result.append(row[::-1])

    return result



print(mirror_matrix([[1, 2, 3], [5, 6]]))
