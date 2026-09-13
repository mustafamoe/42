from collections.abc import Callable


def mage_counter() -> Callable[[], int]:
    count = 0

    def counter() -> int:
        nonlocal count
        count += 1
        return count

    return counter


def spell_accumulator(initial_power: int) -> Callable[[int], int]:
    total_power = initial_power

    def accumulator(power: int) -> int:
        nonlocal total_power
        total_power += power
        return total_power

    return accumulator


def enchantment_factory(enchantment_type: str) -> Callable[[str], str]:
    def enchant(item_name: str) -> str:
        return f"{enchantment_type} {item_name}"

    return enchant


def memory_vault() -> dict[str, Callable[..., object]]:
    memories: dict[str, object] = {}

    def store(key: str, value: object) -> None:
        memories[key] = value

    def recall(key: str) -> object:
        return memories.get(key, "Memory not found")

    return {"store": store, "recall": recall}


def main() -> None:
    counter_a = mage_counter()
    counter_b = mage_counter()
    accumulator = spell_accumulator(100)
    flaming = enchantment_factory("Flaming")
    frozen = enchantment_factory("Frozen")
    vault = memory_vault()

    print("Testing mage counter...")
    print(f"counter_a call 1: {counter_a()}")
    print(f"counter_a call 2: {counter_a()}")
    print(f"counter_b call 1: {counter_b()}")

    print("Testing spell accumulator...")
    print(f"Base 100, add 20: {accumulator(20)}")
    print(f"Base 100, add 30: {accumulator(30)}")

    print("Testing enchantment factory...")
    print(flaming("Sword"))
    print(frozen("Shield"))

    print("Testing memory vault...")
    vault["store"]("secret", 42)
    print("Store 'secret' = 42")
    print(f"Recall 'secret': {vault['recall']('secret')}")
    print(f"Recall 'unknown': {vault['recall']('unknown')}")


if __name__ == "__main__":
    main()
