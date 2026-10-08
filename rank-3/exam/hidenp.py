
def hidenp(small: str, big: str) -> bool:
    i = 0

    if not small:
        return True

    for char in big:
        if char == small[i]:
            i += 1
            if len(small) == i:
                return True

    return False

print(hidenp("abc", "a1b2c3"))  # True
print(hidenp("ace", "abcde"))   # True
print(hidenp("aec", "abcde"))   # False — wrong order
print(hidenp("aa", "abc"))      # False — only one "a"
