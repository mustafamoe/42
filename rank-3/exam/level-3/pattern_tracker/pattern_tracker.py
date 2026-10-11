"""Count adjacent digit pairs that increase by exactly one."""


def pattern_tracker(text: str) -> int:
    """Count overlapping pairs such as 01 and 12, without wrapping 90."""
    count = 0
    for index in range(len(text) - 1):
        first = text[index]
        second = text[index + 1]
        if first in "0123456789" and second in "0123456789":
            if int(second) == int(first) + 1:
                count += 1

    return count
