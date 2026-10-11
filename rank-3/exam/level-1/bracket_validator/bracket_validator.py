"""Validate matching brackets with a stack."""


def bracket_validator(s: str) -> bool:
    """Ignore other characters and check bracket types and nesting."""
    stack: list[str] = []
    pairs = {")": "(", "]": "[", "}": "{"}

    for char in s:
        if char in "([{":
            stack.append(char)
        elif char in pairs:
            # The most recent opening bracket must close first.
            if not stack or stack.pop() != pairs[char]:
                return False

    return not stack
