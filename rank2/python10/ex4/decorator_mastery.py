from collections.abc import Callable
from typing import Any
import functools


# ---------- What this program does ----------
#
# This program demonstrates several powerful Python tools:
#
# 1) Combine numbers in different ways (sum, multiply, max, min)
# 2) Create pre-configured versions of functions
# 3) Speed up slow recursive calculations using caching
# 4) Automatically choose behavior based on input type
#
# The goal is to introduce:
#   - reduce: combine a list into one value
#   - partial: create simpler functions from more complex ones
#   - caching: store previous results to avoid recomputation
#   - singledispatch: change behavior based on input type


# ---------- New Concepts ----------
#
# 1) functools.reduce(function, list):
#    Repeatedly applies a function to combine values.
#    Example: [1, 2, 3] with addition:
#      step1: 1 + 2 = 3
#      step2: 3 + 3 = 6
#
# 2) functools.partial(function, fixed_args...):
#    Creates a new function with some arguments already filled in.
#    Example:
#      base(power, element, target)
#      → partial(base, 50, "fire")
#      → new function: f(target)
#
# 3) @functools.lru_cache:
#    Saves results of previous function calls.
#    If the same input is used again, Python returns the saved result.
#
# 4) @functools.singledispatch:
#    Lets one function behave differently depending on input type.
#    Python automatically chooses the correct version.


# ---------- Spell reducer ----------

def spell_reducer(spells: list[int], operation: str) -> int:
    """
    Combine a list of numbers into a single value based on the operation.
    """
    if not spells:
        return 0

    if operation == "add":
        return functools.reduce(lambda a, b: a + b, spells)

    elif operation == "multiply":
        return functools.reduce(lambda a, b: a * b, spells)

    elif operation == "max":
        return functools.reduce(lambda a, b: a if a > b else b, spells)

    elif operation == "min":
        # Keep the smallest value
        return functools.reduce(lambda a, b: a if a < b else b, spells)

    else:
        raise ValueError(f"Unknown operation: {operation}")


# ---------- Partial enchanter ----------

def partial_enchanter(
    base_enchantment: Callable[[int, str, str], str],
) -> dict[str, Callable[[str], str]]:
    """
    Create ready-to-use enchantment functions with preset values.
    Each returned function only needs a target.
    """
    return {
        "fire": functools.partial(base_enchantment, 50, "fire"),
        "ice": functools.partial(base_enchantment, 50, "ice"),
        "lightning": functools.partial(base_enchantment, 50, "lightning"),
    }


# ---------- Memoized Fibonacci ----------

@functools.lru_cache(maxsize=None)
def memoized_fibonacci(n: int) -> int:
    """
    Compute Fibonacci numbers efficiently using caching.
    """
    if n < 0:
        raise ValueError("Fibonacci cannot be negative")

    if n < 2:
        return n

    return memoized_fibonacci(n - 1) + memoized_fibonacci(n - 2)


def spell_dispatcher() -> Callable[[Any], str]:
    """
    Return a function that behaves differently depending on input type.
    """

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