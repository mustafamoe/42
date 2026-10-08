
def anagram(s1: str, s2: str) -> bool:
    s1 = s1.lower().replace(" ", "")
    s2 = s2.lower().replace(" ", "")

    if len(s1) != len(s2):
        return False

    counts1 = {}
    counts2 = {}

    for c in s1:
        counts1[c] = counts1.get(c, 0) + 1

    for c in s2:
        counts2[c] = counts2.get(c, 0) + 1

    return counts1 == counts2
