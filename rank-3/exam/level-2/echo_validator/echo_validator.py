"""Check whether the letters in a string form a palindrome."""


def echo_validator(text: str) -> bool:
    """Compare letters without case, returning False if there are none."""
    letters: list[str] = []
    for char in text:
        if char.isalpha():
            letters.append(char.lower())

    cleaned = "".join(letters)
    return bool(cleaned) and cleaned == cleaned[::-1]
