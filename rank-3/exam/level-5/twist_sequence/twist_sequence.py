"""Rotate a list to the right using two slices."""


def twist_sequence(arr: list[int], k: int) -> list[int]:
    """Move the final k elements to the front without modifying arr."""
    if not arr:
        return []

    # A full revolution changes nothing, so keep only the remainder.
    k %= len(arr)
    return arr[-k:] + arr[:-k]
