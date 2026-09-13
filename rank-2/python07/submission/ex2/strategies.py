import abc
import typing

from ex0.creature import Creature
from ex1.capabilities import HealCapability
from ex1.capabilities import TransformCapability


class InvalidBattleStrategyError(Exception):
    pass


class BattleStrategy(abc.ABC):
    label = "Strategy"
    strategy_name = "strategy"

    @abc.abstractmethod
    def is_valid(self, creature: Creature) -> bool:
        pass

    @abc.abstractmethod
    def act(self, creature: Creature) -> list[str]:
        pass

    def describe(self) -> str:
        return self.label

    def _raise_invalid(self, creature: Creature) -> None:
        message = (
            f"Invalid Creature '{creature.name}' "
            f"for this {self.strategy_name} strategy"
        )
        raise InvalidBattleStrategyError(message)


class NormalStrategy(BattleStrategy):
    label = "Normal"
    strategy_name = "normal"

    def is_valid(self, creature: Creature) -> bool:
        return True

    def act(self, creature: Creature) -> list[str]:
        return [creature.attack()]


class AggressiveStrategy(BattleStrategy):
    label = "Aggressive"
    strategy_name = "aggressive"

    def is_valid(self, creature: Creature) -> bool:
        return isinstance(creature, TransformCapability)

    def act(self, creature: Creature) -> list[str]:
        if not self.is_valid(creature):
            self._raise_invalid(creature)

        transformable = typing.cast(TransformCapability, creature)
        return [
            transformable.transform(),
            creature.attack(),
            transformable.revert(),
        ]


class DefensiveStrategy(BattleStrategy):
    label = "Defensive"
    strategy_name = "defensive"

    def is_valid(self, creature: Creature) -> bool:
        return isinstance(creature, HealCapability)

    def act(self, creature: Creature) -> list[str]:
        if not self.is_valid(creature):
            self._raise_invalid(creature)

        healer = typing.cast(HealCapability, creature)
        return [
            creature.attack(),
            healer.heal(),
        ]
