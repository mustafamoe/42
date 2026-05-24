import alchemy.grimoire as grimoire


def main() -> None:
    print("=== Kaboom 0 ===")
    print("Using grimoire module directly")
    print(
        "Testing record light spell: "
        f"{grimoire.light_spell_record('Fantasy', 'Earth, wind and fire')}"
    )


if __name__ == "__main__":
    main()
