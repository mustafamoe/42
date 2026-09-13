def artifact_sorter(artifacts: list[dict]) -> list[dict]:
    return sorted(
        artifacts,
        key=lambda artifact: artifact["power"],
        reverse=True,
    )


def power_filter(mages: list[dict], min_power: int) -> list[dict]:
    return list(filter(lambda mage: mage["power"] >= min_power, mages))


def spell_transformer(spells: list[str]) -> list[str]:
    return list(map(lambda spell: f"* {spell} *", spells))


def mage_stats(mages: list[dict]) -> dict:
    if not mages:
        return {"max_power": 0, "min_power": 0, "avg_power": 0.0}

    return {
        "max_power": max(mages, key=lambda mage: mage["power"])["power"],
        "min_power": min(mages, key=lambda mage: mage["power"])["power"],
        "avg_power": round(
            sum(map(lambda mage: mage["power"], mages)) / len(mages),
            2,
        ),
    }


def main() -> None:
    artifacts = [
        {"name": "Crystal Orb", "power": 85, "type": "focus"},
        {"name": "Fire Staff", "power": 92, "type": "weapon"},
        {"name": "Wind Cloak", "power": 71, "type": "accessory"},
    ]
    mages = [
        {"name": "Alex", "power": 95, "element": "fire"},
        {"name": "Riley", "power": 63, "element": "ice"},
        {"name": "Sage", "power": 78, "element": "wind"},
    ]
    spells = ["fireball", "heal", "shield"]

    sorted_artifacts = artifact_sorter(artifacts)
    transformed_spells = spell_transformer(spells)
    powerful_mages = power_filter(mages, 75)

    print("Testing artifact sorter...")
    print(
        f"{sorted_artifacts[0]['name']} "
        f"({sorted_artifacts[0]['power']} power) "
        f"comes before {sorted_artifacts[1]['name']} "
        f"({sorted_artifacts[1]['power']} power)"
    )

    print("Testing spell transformer...")
    print(" ".join(transformed_spells))

    print("Testing power filter...")
    print(", ".join(map(lambda mage: mage["name"], powerful_mages)))

    print("Testing mage stats...")
    print(mage_stats(mages))


if __name__ == "__main__":
    main()
