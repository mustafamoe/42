from ex0.factories import CreatureFactory
from ex1.creatures import HealingCreature
from ex1.creatures import Bloomelle as _Bloomelle
from ex1.creatures import Morphagon as _Morphagon
from ex1.creatures import Shiftling as _Shiftling
from ex1.creatures import Sproutling as _Sproutling
from ex1.creatures import TransformingCreature


class HealingCreatureFactory(CreatureFactory):
    def create_base(self) -> HealingCreature:
        return _Sproutling()

    def create_evolved(self) -> HealingCreature:
        return _Bloomelle()


class TransformCreatureFactory(CreatureFactory):
    def create_base(self) -> TransformingCreature:
        return _Shiftling()

    def create_evolved(self) -> TransformingCreature:
        return _Morphagon()
