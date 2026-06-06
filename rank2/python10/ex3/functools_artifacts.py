from collections.abc import Callable
from typing import Any
import functools


# ---------- What this program does ----------
#
# This program shows more advanced "magic tools":
#   - Combine numbers in different ways (sum, multiply, max, min)
#   - Create pre-configured enchantment functions
#   - Speed up slow calculations (Fibonacci) using caching
#   - Automatically choose behavior based on input type
#
# The goal is to introduce:
#   - reduce (combining a list into one value)
#   - partial (pre-filling function arguments)
#   - caching (remembering previous results)
#   - function overloading (different behavior per type)


# ---------- New Concepts ----------
#
# 1) functools.reduce:
#    Combines a list into a single value step by step.
#    Example: [1, 2, 3] with addition → ((1 + 2) + 3) = 6
#
# 2) functools.partial:
#    Creates a new function with some arguments already filled in.
#    Example: fixing "power=50" and "element='fire'"
#
# 3) @lru_cache:
#    Stores results of function calls so repeated work is avoided.
#    Makes recursive functions like Fibonacci much faster.
#
# 4) @singledispatch:
#    Lets one function behave differently depending on input type.
#    Example: int → damage spell, str → enchantment, list → multi-cast.



def spell_reducer(spells: list[int], operation: str) -> int:
    if not spells:
        return 0

    if operation == "add":
        return functools.reduce(lambda a, b: a + b, spells)

    elif operation == "multiply":
        return functools.reduce(lambda a, b: a * b, spells)

    elif operation == "max":
        return functools.reduce(lambda a, b: a if a > b else b, spells)

    elif operation == "min":
        return functools.reduce(lambda a, b: a if a < b else b, spells)

    else:
        raise ValueError(f"Unknown operation: {operation}")


def partial_enchanter(
    base_enchantment: Callable[[int, str, str], str],
) -> dict[str, Callable[[str], str]]:
    return {
        "fire": functools.partial(base_enchantment, 50, "fire"),
        "ice": functools.partial(base_enchantment, 50, "ice"),
        "lightning": functools.partial(base_enchantment, 50, "lightning"),
    }


@functools.lru_cache(maxsize=None)
def memoized_fibonacci(n: int) -> int:
    if n < 0:
        raise ValueError("Fibonacci cannot be negative")

    if n < 2:
        return n

    return memoized_fibonacci(n - 1) + memoized_fibonacci(n - 2)


def spell_dispatcher() -> Callable[[Any], str]:

    @functools.singledispatch
    def dispatch(spell: Any) -> str:
        return "Unknown spell type"

    @dispatch.register
    def _(spell: int) -> str:
        return f"Damage spell: {spell} damage"

    @dispatch.register
    def _(spell: str) -> str:
        return f"Enchantment: {spell}"

    @dispatch.register
    def _(spell: list) -> str:
        return f"Multi-cast: {len(spell)} spells"

    return dispatch


def base_enchantment(power: int, element: str, target: str) -> str:
    return f"{target} gains {power} {element} power"


if __name__ == "__main__":
    spells = [10, 20, 30, 40]
    enchanters = partial_enchanter(base_enchantment)
    dispatcher = spell_dispatcher()

    print("Testing spell reducer...")
    print("Sum:", spell_reducer(spells, "add"))
    print("Product:", spell_reducer(spells, "multiply"))
    print("Max:", spell_reducer(spells, "max"))

    print("\nTesting partial enchanter...")
    print(enchanters["fire"]("Sword"))

    print("\nTesting memoized fibonacci...")
    print("Fib(10):", memoized_fibonacci(10))
    print("Fib(15):", memoized_fibonacci(15))

    print("\nTesting spell dispatcher...")
    print(dispatcher(42))
    print(dispatcher("fireball"))
    print(dispatcher(["fireball", "heal"]))
    print(dispatcher({"unknown": True}))