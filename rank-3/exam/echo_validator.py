
def echo_validator(text: str) -> bool:
    cleaned = ""

    for char in text:
        if char.isalpha():
            cleaned += char.lower()

    if not cleaned:
        return False

    if cleaned == cleaned[::-1]:
        return True

    return False

print(echo_validator("Racecar"))
print(echo_validator("123!"))
