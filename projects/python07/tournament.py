import typing

from ex0 import AquaFactory
from ex0 import CreatureFactory
from ex0 import FlameFactory
from ex0.creature import Creature
from ex1 import HealingCreatureFactory
from ex1 import TransformCreatureFactory
from ex2 import AggressiveStrategy
from ex2 import BattleStrategy
from ex2 import DefensiveStrategy
from ex2 import InvalidBattleStrategyError
from ex2 import NormalStrategy

Opponent = typing.Tuple[CreatureFactory, BattleStrategy]
Participant = typing.Tuple[Creature, BattleStrategy]


def factory_label(factory: CreatureFactory) -> str:
    if isinstance(factory, HealingCreatureFactory):
        return "Healing"
    if isinstance(factory, TransformCreatureFactory):
        return "Transform"
    return factory.create_base().name


def print_roster(opponents: list[Opponent]) -> None:
    entries: list[str] = []
    for factory, strategy in opponents:
        entries.append(f"({factory_label(factory)}+{strategy.describe()})")
    print(f"[ {', '.join(entries)} ]")


def prepare_participants(opponents: list[Opponent]) -> list[Participant]:
    participants: list[Participant] = []
    for factory, strategy in opponents:
        participants.append((factory.create_base(), strategy))
    return participants


def run_actions(creature: Creature, strategy: BattleStrategy) -> None:
    actions = strategy.act(creature)
    for action in actions:
        print(action)


def battle(opponents: list[Opponent]) -> None:
    participants = prepare_participants(opponents)

    print("*** Tournament ***")
    print(f"{len(participants)} opponents involved")

    for first_index, first in enumerate(participants):
        first_creature, first_strategy = first
        remaining = participants[first_index + 1:]

        for second_creature, second_strategy in remaining:
            print("* Battle *")
            print(first_creature.describe())
            print("vs.")
            print(second_creature.describe())
            print("now fight!")

            try:
                run_actions(first_creature, first_strategy)
                run_actions(second_creature, second_strategy)
            except InvalidBattleStrategyError as error:
                print(f"Battle error, aborting tournament: {error}")
                return


def main() -> None:
    tournament_0 = [
        (FlameFactory(), NormalStrategy()),
        (HealingCreatureFactory(), DefensiveStrategy()),
    ]
    tournament_1 = [
        (FlameFactory(), AggressiveStrategy()),
        (HealingCreatureFactory(), DefensiveStrategy()),
    ]
    tournament_2 = [
        (AquaFactory(), NormalStrategy()),
        (HealingCreatureFactory(), DefensiveStrategy()),
        (TransformCreatureFactory(), AggressiveStrategy()),
    ]

    print("Tournament 0 (basic)")
    print_roster(tournament_0)
    battle(tournament_0)
    print("Tournament 1 (error)")
    print_roster(tournament_1)
    battle(tournament_1)
    print("Tournament 2 (multiple)")
    print_roster(tournament_2)
    battle(tournament_2)


if __name__ == "__main__":
    main()
