from ex0 import AquaFactory
from ex0 import CreatureFactory
from ex0 import FlameFactory


def test_factory(factory: CreatureFactory) -> None:
    base = factory.create_base()
    evolved = factory.create_evolved()

    print("Testing factory")
    print(base.describe())
    print(base.attack())
    print(evolved.describe())
    print(evolved.attack())


def test_battle(
    first_factory: CreatureFactory,
    second_factory: CreatureFactory,
) -> None:
    first = first_factory.create_base()
    second = second_factory.create_base()

    print("Testing battle")
    print(first.describe())
    print("vs.")
    print(second.describe())
    print("fight!")
    print(first.attack())
    print(second.attack())


def main() -> None:
    flame_factory = FlameFactory()
    aqua_factory = AquaFactory()

    test_factory(flame_factory)
    test_factory(aqua_factory)
    test_battle(aqua_factory, flame_factory)
    test_battle(flame_factory, aqua_factory)


if __name__ == "__main__":
    main()
