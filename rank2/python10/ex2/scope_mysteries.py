# What this program does:
#
# This program shows how to build small "magic tools" using functions that
# create other functions. Each tool is like a magical gadget:
#   - A mage counter that counts how many times a mage casts spells.
#   - A spell accumulator that keeps adding up total power over time.
#   - An enchantment factory that makes words like "Flaming Sword".
#   - A memory vault that stores and recalls values by name.
#
# The main goal is to learn:
#   - functions that return other functions
#   - "nonlocal" variables (variables inside nested functions)
#   - simple factories that create customized tools
#   - a tiny dictionary-based storage system (store/recall)

from collections.abc import Callable
from typing import Any


# ---------- New Concepts (quick overview) ----------
#
# 1) Function that returns a function:
#    These tools (like mage_counter) create and return a new function each time.
#    The returned function remembers its own private data.
#
# 2) nonlocal:
#    Inside a nested function (a function inside another function), `nonlocal`
#    lets you modify a variable from the outer function (like `count` or `total_power`).
#
# 3) Callable type hint:
#    `Callable[[], int]` means "a function that takes no arguments and returns an int".
#    `Callable[[int], int]` means "a function that takes one int and returns an int".
#
# 4) Lambda / simple functions as data:
#    We treat functions like Anys: we can create them, store them, and pass them around.
#
# 5) Dictionary as a tiny vault:
#    The `memory_vault` uses a dictionary to store values under string keys, like a
#    simple database: store(key, value) and recall(key).


def mage_counter() -> Callable[[], int]:
    """
    Creates a counter that tracks how many times it's called.
    Each call returns 1, 2, 3, ... independently for each counter.
    """
    count = 0

    def counter() -> int:
        nonlocal count
        count += 1
        return count

    return counter


def spell_accumulator(initial_power: int) -> Callable[[int], int]:
    """
    Creates an accumulator that keeps adding power to a total.
    Starts at `initial_power`, then adds each new power value.
    """
    total_power = initial_power

    def accumulator(power: int) -> int:
        nonlocal total_power
        total_power += power
        return total_power

    return accumulator


def enchantment_factory(enchantment_type: str) -> Callable[[str], str]:
    """
    Creates an enchantment function that adds a type to an item name.
    Example: Flaming("Sword") -> "Flaming Sword"
    """
    def enchant(item_name: str) -> str:
        return f"{enchantment_type} {item_name}"

    return enchant


def memory_vault() -> dict[str, Callable]:
    """
    Creates a tiny storage system with two functions:
      - store(key, value): save a value under a name
      - recall(key): get the value back, or "Memory not found" if missing

    Returns a dictionary: {"store": store, "recall": recall}
    """
    memories: dict[str, Any] = {}

    def store(key: str, value: Any) -> None:
        memories[key] = value

    def recall(key: str) -> Any:
        return memories.get(key, "Memory not found")

    return {"store": store, "recall": recall}


if __name__ == "__main__":
    counter_a = mage_counter()
    counter_b = mage_counter()
    accumulator = spell_accumulator(100)
    flaming = enchantment_factory("Flaming")
    frozen = enchantment_factory("Frozen")
    vault = memory_vault()
    vault1 = memory_vault()

    print("Testing mage counter...")
    print(f"counter_a call 1: {counter_a()}")
    print(f"counter_a call 2: {counter_a()}")
    print(f"counter_b call 1: {counter_b()}")

    print("\nTesting spell accumulator...")
    print(f"Base 100, add 20: {accumulator(20)}")
    print(f"Base 100, add 30: {accumulator(30)}")

    print("\nTesting enchantment factory...")
    print(flaming("Sword"))
    print(frozen("Shield"))

    print("\nTesting memory vault...")
    vault["store"]("secret", 42)
    print("Store 'secret' = 42")
    print(f"Recall 'secret': {vault['recall']('secret')}")
    print(f"Recall 'unknown': {vault['recall']('unknown')}")
