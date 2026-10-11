"""Compare exact character counts, including case and whitespace."""


def string_permutation_checker(s1: str, s2: str) -> bool:
    """Return whether rearranging s1 can produce s2 without editing it."""
    if len(s1) != len(s2):
        return False

    first_counts: dict[str, int] = {}
    second_counts: dict[str, int] = {}
    for char in s1:
        first_counts[char] = first_counts.get(char, 0) + 1
    for char in s2:
        second_counts[char] = second_counts.get(char, 0) + 1

    return first_counts == second_counts
