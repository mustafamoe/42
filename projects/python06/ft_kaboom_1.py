def main() -> None:
    print("=== Kaboom 1 ===", flush=True)
    print("Access to alchemy/grimoire/dark_spellbook.py directly", flush=True)
    print(
        "Test import now - THIS WILL RAISE AN UNCAUGHT EXCEPTION",
        flush=True,
    )
    from alchemy.grimoire.dark_spellbook import dark_spell_record

    print(
        "Testing record dark spell: "
        f"{dark_spell_record('Nightfall', 'Bats and fog')}"
    )


if __name__ == "__main__":
    main()
