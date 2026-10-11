"""Alternate letter case, restarting after each ordinary space."""


def string_sculptor(text: str) -> str:
    """Count only letters; leave digits and punctuation unchanged."""
    result = ""
    letter_index = 0
    for char in text:
        if char == " ":
            letter_index = 0

        if char.isalpha():
            result += char.lower() if letter_index % 2 == 0 else char.upper()
            letter_index += 1
        else:
            result += char

    return result
