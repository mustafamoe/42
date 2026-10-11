"""Sort strings by the required keys without built-in sorting."""


def cryptic_sorter(strings: list[str]) -> list[str]:
    """Return a stable ordering by length, lowercase text, and vowel count."""
    def sort_key(word: str) -> tuple[int, str, int]:
        lowered = word.lower()
        vowels = sum(char in "aeiou" for char in lowered)
        return len(word), lowered, vowels

    result: list[str] = []
    for word in strings:
        position = 0
        word_key = sort_key(word)
        # Insert after equal keys to preserve their original order.
        while (
            position < len(result)
            and sort_key(result[position]) <= word_key
        ):
            position += 1
        result.insert(position, word)

    return result
