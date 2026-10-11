"""Merge two ascending lists while keeping all duplicate values."""


def shadow_merge(list1: list[int], list2: list[int]) -> list[int]:
    """Build a sorted result by choosing the smaller next value."""
    result: list[int] = []
    left_index = 0
    right_index = 0

    while left_index < len(list1) and right_index < len(list2):
        if list1[left_index] <= list2[right_index]:
            result.append(list1[left_index])
            left_index += 1
        else:
            result.append(list2[right_index])
            right_index += 1

    # Once one list is exhausted, the other remainder is already sorted.
    result.extend(list1[left_index:])
    result.extend(list2[right_index:])
    return result
