"""Shift English letters around the alphabet with a Caesar cipher."""


def whisper_cipher(text: str, shift: int) -> str:
    """Shift letters in either direction, preserving case and other text."""
    result = ""
    for char in text:
        if "a" <= char <= "z":
            result += chr((ord(char) - ord("a") + shift) % 26 + ord("a"))
        elif "A" <= char <= "Z":
            result += chr((ord(char) - ord("A") + shift) % 26 + ord("A"))
        else:
            result += char

    return result
