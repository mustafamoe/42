
def shadow_merge(list1: list[int], list2: list[int]) -> list[int]:
    result = []
    j = 0
    k = 0

    while j < len(list1) and k < len(list2):
        if list1[j] <= list2[k]:
            result.append(list1[j])
            j += 1
        else:
            result.append(list2[k])
            k += 1

    result.extend(list1[j:])
    result.extend(list2[k:])

    return result
