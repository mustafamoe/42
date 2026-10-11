"""Find distinct shared characters in the first string's order."""


def inter(s1: str, s2: str) -> str:
    """Return each shared character once, preserving its first occurrence."""
    result = ""
    for char in s1:
        if char in s2 and char not in result:
            result += char

    return result
