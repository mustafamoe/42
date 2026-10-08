
def string_sculptor(text: str) -> str:
    result = ""
    index = 0

    for char in text:
        if char == " ":
            index = 0

        if char.isalpha():
            result += char.lower() if index % 2 == 0 else char.upper()
            index += 1
        else:
            result += char

    return result
