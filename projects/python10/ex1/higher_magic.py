from collections.abc import Callable


def spell_combiner(
    spell1: Callable[[str, int], str],
    spell2: Callable[[str, int], str],
) -> Callable[[str, int], tuple[str, str]]:
    if not callable(spell1) or not callable(spell2):
        raise TypeError("Spells must be callable")

    def combined_spell(target: str, power: int) -> tuple[str, str]:
        return spell1(target, power), spell2(target, power)

    return combined_spell


def power_amplifier(
    base_spell: Callable[[str, int], str],
    multiplier: int,
) -> Callable[[str, int], str]:
    if not callable(base_spell):
        raise TypeError("Spell must be callable")

    def amplified_spell(target: str, power: int) -> str:
        return base_spell(target, power * multiplier)

    return amplified_spell


def conditional_caster(
    condition: Callable[[str, int], bool],
    spell: Callable[[str, int], str],
) -> Callable[[str, int], str]:
    if not callable(condition) or not callable(spell):
        raise TypeError("Condition and spell must be callable")

    def conditional_spell(target: str, power: int) -> str:
        if condition(target, power):
            return spell(target, power)
        return "Spell fizzled"

    return conditional_spell


def spell_sequence(
    spells: list[Callable[[str, int], str]],
) -> Callable[[str, int], list[str]]:
    if not all(callable(spell) for spell in spells):
        raise TypeError("All spells must be callable")

    def sequenced_spell(target: str, power: int) -> list[str]:
        return [spell(target, power) for spell in spells]

    return sequenced_spell


def fireball(target: str, power: int) -> str:
    return f"Fireball hits {target} for {power} damage"


def heal(target: str, power: int) -> str:
    return f"Heal restores {target} for {power} HP"


def shield(target: str, power: int) -> str:
    return f"Shield protects {target} with {power} power"


def enough_power(target: str, power: int) -> bool:
    return power >= 10 and bool(target)


def main() -> None:
    combined = spell_combiner(fireball, heal)
    mega_fireball = power_amplifier(fireball, 3)
    safe_shield = conditional_caster(enough_power, shield)
    full_sequence = spell_sequence([fireball, heal, shield])

    print("Testing spell combiner...")
    print(f"Combined spell result: {combined('Dragon', 20)}")

    print("Testing power amplifier...")
    print(f"Original: {fireball('Dragon', 10)}")
    print(f"Amplified: {mega_fireball('Dragon', 10)}")

    print("Testing conditional caster...")
    print(safe_shield("Dragon", 5))
    print(safe_shield("Dragon", 15))

    print("Testing spell sequence...")
    print(full_sequence("Dragon", 12))


if __name__ == "__main__":
    main()
