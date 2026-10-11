"""Convert nonnegative integer strings between bases 2 through 36."""


def number_base_converter(number: str, from_base: int, to_base: int) -> str:
    """Return uppercase digits in the target base, or ERROR for bad input."""
    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if not number or not number.isascii():
        return "ERROR"
    if not (2 <= from_base <= 36 and 2 <= to_base <= 36):
        return "ERROR"

    number = number.upper()
    if any(char not in digits[:from_base] for char in number):
        return "ERROR"

    # Positional notation also avoids int()'s limit on long decimal strings.
    value = 0
    for char in number:
        value = value * from_base + digits.index(char)
    result = ""
    while value:
        # Remainders produce digits from right to left.
        value, remainder = divmod(value, to_base)
        result = digits[remainder] + result

    return result or "0"
