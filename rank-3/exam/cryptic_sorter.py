
def cryptic_sorter(strings: list[str]) -> list[str]:
    def key(word: str) -> tuple[int, str, int]:
        lowered = word.lower()
        vowles = sum(char in ("uaeio") for char in lowered)
        return (len(word), lowered, vowles)

    result = []
    for word in strings:
        position = 0
        word_key = key(word)
        while position < len(result) and key(result[position]) <= word_key:
            position += 1
        result.insert(position, word)

    return result
