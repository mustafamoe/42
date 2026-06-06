from collections.abc import Callable

Spell = Callable[[str, int], str]
Condition = Callable[[str, int], bool]


def spell_combiner(spell1: Spell, spell2: Spell) -> Callable[[str, int], tuple[str, str]]:
    if not all(map(callable, (spell1, spell2))):
        raise TypeError("Spells must be callable")

    def combined(target: str, power: int) -> tuple[str, str]:
        return spell1(target, power), spell2(target, power)

    return combined


def power_amplifier(base_spell: Spell, multiplier: int) -> Spell:
    if not callable(base_spell):
        raise TypeError("Spell must be callable")

    def amplified(target: str, power: int) -> str:
        return base_spell(target, power * multiplier)

    return amplified


def conditional_caster(condition: Condition, spell: Spell) -> Spell:
    if not all(map(callable, (condition, spell))):
        raise TypeError("Condition and spell must be callable")

    def cast(target: str, power: int) -> str:
        return spell(target, power) if condition(target, power) else "Spell fizzled"

    return cast


def spell_sequence(spells: list[Spell]) -> Callable[[str, int], list[str]]:
    if not all(map(callable, spells)):
        raise TypeError("All spells must be callable")

    def sequence(target: str, power: int) -> list[str]:
        return [spell(target, power) for spell in spells]

    return sequence


def fireball(target: str, power: int) -> str:
    return f"Fireball hits {target} for {power} damage"


def heal(target: str, power: int) -> str:
    return f"Heal restores {target} for {power} HP"


def shield(target: str, power: int) -> str:
    return f"Shield protects {target} with {power} power"


def enough_power(target: str, power: int) -> bool:
    return power >= 10 and bool(target)


if __name__ == "__main__":
    combined = spell_combiner(fireball, heal)
    mega_fireball = power_amplifier(fireball, 3)
    safe_shield = conditional_caster(enough_power, shield)
    full_sequence = spell_sequence([fireball, heal, shield])

    print("Testing spell combiner...")
    print(combined("Dragon", 20))

    print("\nTesting power amplifier...")
    print("Original:", fireball("Dragon", 10))
    print("Amplified:", mega_fireball("Dragon", 10))

    print("\nTesting conditional caster...")
    print(safe_shield("Dragon", 5))
    print(safe_shield("Dragon", 15))

    print("\nTesting spell sequence...")
    print(full_sequence("Dragon", 12))
