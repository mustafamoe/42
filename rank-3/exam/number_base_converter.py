
def number_base_converter(number: str, from_base: int, to_base: int) -> str:
    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    number = number.upper()
    if not number or not (2 <= from_base <= 36 and 2 <= to_base <= 36):
        return "ERROR"
    if any(c not in digits[:from_base] for c in number):
        return "ERROR"
    value = int(number, from_base)
    result = ""
    while value:
        value, remainder = divmod(value, to_base)
        result = digits[remainder] + result
    return result or "0"


print(number_base_converter("1010", 2, 10))  # "10"
print(number_base_converter("FF", 16, 10))    # "255"
print(number_base_converter("255", 10, 16))   # "FF"
print(number_base_converter("35", 10, 36))    # "Z"
print(number_base_converter("G", 16, 10))     # "ERROR": G means 16
print(number_base_converter("123", 1, 10))    # "ERROR": invalid base
