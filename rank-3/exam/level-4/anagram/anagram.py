"""Compare character counts after ignoring case and ordinary spaces."""


def anagram(s1: str, s2: str) -> bool:
    """Return whether the normalized strings contain the same characters."""
    s1 = s1.lower().replace(" ", "")
    s2 = s2.lower().replace(" ", "")

    if len(s1) != len(s2):
        return False

    first_counts: dict[str, int] = {}
    second_counts: dict[str, int] = {}
    for char in s1:
        first_counts[char] = first_counts.get(char, 0) + 1
    for char in s2:
        second_counts[char] = second_counts.get(char, 0) + 1

    return first_counts == second_counts
