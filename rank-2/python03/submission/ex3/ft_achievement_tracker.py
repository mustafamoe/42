import random


ACHIEVEMENTS = [
    "First Steps",
    "Boss Slayer",
    "Treasure Hunter",
    "Speed Runner",
    "Master Explorer",
    "Crafting Genius",
    "Survivor",
    "Untouchable",
    "World Savior",
    "Collector Supreme",
    "Strategist",
    "Hidden Path Finder",
    "Sharp Mind",
    "Unstoppable",
]


def gen_player_achievements() -> set[str]:
    achievement_count = random.randint(5, 9)
    return set(random.sample(ACHIEVEMENTS, achievement_count))


def print_unique_achievements(
    player_name: str,
    player_achievements: set[str],
    other_achievements: set[str],
) -> None:
    unique_achievements = player_achievements.difference(other_achievements)
    print(f"Only {player_name} has: {unique_achievements}")


def main() -> None:
    print("=== Achievement Tracker System ===")
    alice = gen_player_achievements()
    bob = gen_player_achievements()
    charlie = gen_player_achievements()
    dylan = gen_player_achievements()

    print(f"Player Alice: {alice}")
    print(f"Player Bob: {bob}")
    print(f"Player Charlie: {charlie}")
    print(f"Player Dylan: {dylan}")

    all_achievements = alice.union(bob).union(charlie).union(dylan)
    common_achievements = alice.intersection(bob).intersection(charlie)
    common_achievements = common_achievements.intersection(dylan)

    print(f"All distinct achievements: {all_achievements}")
    print(f"Common achievements: {common_achievements}")

    print_unique_achievements("Alice", alice, bob.union(charlie).union(dylan))
    print_unique_achievements("Bob", bob, alice.union(charlie).union(dylan))
    other_achievements = alice.union(bob).union(dylan)
    print_unique_achievements("Charlie", charlie, other_achievements)
    print_unique_achievements("Dylan", dylan, alice.union(bob).union(charlie))

    achievement_goal = set(ACHIEVEMENTS)
    print(f"Alice is missing: {achievement_goal.difference(alice)}")
    print(f"Bob is missing: {achievement_goal.difference(bob)}")
    print(f"Charlie is missing: {achievement_goal.difference(charlie)}")
    print(f"Dylan is missing: {achievement_goal.difference(dylan)}")


if __name__ == "__main__":
    main()
