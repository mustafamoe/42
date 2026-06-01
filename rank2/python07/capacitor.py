from ex1 import HealingCreatureFactory
from ex1 import TransformCreatureFactory


def test_healing_factory(factory: HealingCreatureFactory) -> None:
   
    base = factory.create_base()
    print("Testing Creature with healing capability")
    print("base:")
    print(base.describe())
    print(base.attack())
    print(base.heal())

    evolved = factory.create_evolved()
    print("evolved:")
    print(evolved.describe())
    print(evolved.attack())
    print(evolved.heal())


def test_transform_factory(factory: TransformCreatureFactory) -> None:
    
    base = factory.create_base()
    print("Testing Creature with transform capability")
    print("base:")
    print(base.describe())
    print(base.attack())
    print(base.transform())
    print(base.attack())
    print(base.revert())

    evolved = factory.create_evolved()
    print("evolved:")
    print(evolved.describe())
    print(evolved.attack())
    print(evolved.transform())
    print(evolved.attack())
    print(evolved.revert())


if __name__ == "__main__":
    test_healing_factory(HealingCreatureFactory())
    test_transform_factory(TransformCreatureFactory())
