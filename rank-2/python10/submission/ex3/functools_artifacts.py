from collections.abc import Callable
from typing import Any

import functools
import operator


def spell_reducer(spells: list[int], operation: str) -> int:
    if not spells:
        return 0

    if operation == "add":
        return functools.reduce(operator.add, spells)
    if operation == "multiply":
        return functools.reduce(operator.mul, spells)
    if operation == "max":
        return functools.reduce(
            lambda current, power: current if operator.gt(current, power)
            else power,
            spells,
        )
    if operation == "min":
        return functools.reduce(
            lambda current, power: current if operator.lt(current, power)
            else power,
            spells,
        )

    raise ValueError(f"Unknown spell reduction operation: {operation}")


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
        raise ValueError("Fibonacci number cannot be negative")
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


def main() -> None:
    spells = [10, 20, 30, 40]
    enchanters = partial_enchanter(base_enchantment)
    dispatcher = spell_dispatcher()

    print("Testing spell reducer...")
    print(f"Sum: {spell_reducer(spells, 'add')}")
    print(f"Product: {spell_reducer(spells, 'multiply')}")
    print(f"Max: {spell_reducer(spells, 'max')}")

    print("Testing partial enchanter...")
    print(enchanters["fire"]("Sword"))

    print("Testing memoized fibonacci...")
    print(f"Fib(0): {memoized_fibonacci(0)}")
    print(f"Fib(1): {memoized_fibonacci(1)}")
    print(f"Fib(10): {memoized_fibonacci(10)}")
    print(f"Fib(15): {memoized_fibonacci(15)}")

    print("Testing spell dispatcher...")
    print(dispatcher(42))
    print(dispatcher("fireball"))
    print(dispatcher(["fireball", "heal", "shield"]))
    print(dispatcher({"unknown": True}))


if __name__ == "__main__":
    main()
