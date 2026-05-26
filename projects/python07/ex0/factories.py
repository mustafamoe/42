import abc

from ex0.creature import Creature
from ex0.creatures import Aquabub as _Aquabub
from ex0.creatures import Flameling as _Flameling
from ex0.creatures import Pyrodon as _Pyrodon
from ex0.creatures import Torragon as _Torragon


class CreatureFactory(abc.ABC):
    @abc.abstractmethod
    def create_base(self) -> Creature:
        pass

    @abc.abstractmethod
    def create_evolved(self) -> Creature:
        pass


class FlameFactory(CreatureFactory):
    def create_base(self) -> Creature:
        return _Flameling()

    def create_evolved(self) -> Creature:
        return _Pyrodon()


class AquaFactory(CreatureFactory):
    def create_base(self) -> Creature:
        return _Aquabub()

    def create_evolved(self) -> Creature:
        return _Torragon()
