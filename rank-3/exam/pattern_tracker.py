
def pattern_tracker(text: str) -> int:
    count = 0

    for i in range(len(text) - 1):
        first = text[i]
        second = text[i + 1]

        if first in "0123456789" and second in "0123456789":
            if int(second) == int(first) + 1:
                count += 1

    return count
