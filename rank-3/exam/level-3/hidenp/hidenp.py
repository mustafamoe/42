"""Look for an ordered subsequence inside another string."""


def hidenp(small: str, big: str) -> bool:
    """Return whether every character of small can be matched in order."""
    if not small:
        return True

    small_index = 0
    for char in big:
        if char == small[small_index]:
            small_index += 1
            # Stop before the next iteration could index past small.
            if small_index == len(small):
                return True

    return False
