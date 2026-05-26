# Python Module 07 Notes

## Big idea

This module is about abstract architecture for creature cards.

The goal is to practice:

- abstract base classes
- abstract factories
- separated capabilities
- strategy objects
- package interfaces

## Global rules

Subject requirements:

- Python 3.10 or later.
- Code must pass `flake8`.
- Code must include type annotations and pass `mypy`.
- Standard classes, collections, and methods are allowed.
- Built-in functions are allowed except `eval()` and `exec()`.
- Functions should handle exceptions gracefully.
- External libraries are forbidden.
- Each exercise folder must include `__init__.py`.
- Testing scripts are located at the project root.

Authorized imports used here:

- project modules
- `abc`
- `typing`

Not allowed:

- external libraries
- `eval()`
- `exec()`
- exposing concrete Creature classes through `ex0` or `ex1`

## Exercise 0: Creature Factory

Files:

- `battle.py`
- `ex0/__init__.py`
- `ex0/creature.py`
- `ex0/creatures.py`
- `ex0/factories.py`

Subject requirements:

- `Creature` is abstract.
- `Creature` stores the Creature name and type.
- `Creature.attack()` is abstract.
- `Creature.describe()` returns the standard description message.
- `Flameling`, `Pyrodon`, `Aquabub`, and `Torragon` inherit from `Creature`.
- `CreatureFactory` is abstract.
- `CreatureFactory.create_base()` creates the base family Creature.
- `CreatureFactory.create_evolved()` creates the evolved family Creature.
- `FlameFactory` creates `Flameling` and `Pyrodon`.
- `AquaFactory` creates `Aquabub` and `Torragon`.
- `battle.py` tests both factories with one reusable function.
- `battle.py` makes two base Creatures fight.

Allowed:

- builtins
- standard types
- `abc`
- `typing`
- project imports

Not allowed:

- external libraries
- `eval()`
- `exec()`
- exposing concrete Creature classes from `ex0/__init__.py`

## Exercise 1: Capabilities

Files:

- `capacitor.py`
- `ex1/__init__.py`
- `ex1/capabilities.py`
- `ex1/creatures.py`
- `ex1/factories.py`

Subject requirements:

- Build on `ex0`.
- `HealCapability` is separate from `Creature`.
- `HealCapability.heal()` is abstract.
- `TransformCapability` is separate from `Creature`.
- `TransformCapability.transform()` is abstract.
- `TransformCapability.revert()` is abstract.
- Transforming Creatures keep persistent transform state.
- Transform state changes the `attack()` result.
- `Sproutling` and `Bloomelle` inherit from `Creature` and `HealCapability`.
- `HealingCreatureFactory` creates `Sproutling` and `Bloomelle`.
- `Shiftling` and `Morphagon` inherit from `Creature` and `TransformCapability`.
- `TransformCreatureFactory` creates `Shiftling` and `Morphagon`.
- `capacitor.py` demonstrates describe, attack, heal, transform, and revert.

Allowed:

- builtins
- standard types
- `abc`
- `typing`
- project imports

Not allowed:

- external libraries
- `eval()`
- `exec()`
- making capability classes inherit from `Creature`
- exposing concrete Creature classes from `ex1/__init__.py`

## Exercise 2: Abstract Strategy

Files:

- `tournament.py`
- `ex2/__init__.py`
- `ex2/strategies.py`

Subject requirements:

- `BattleStrategy` is abstract.
- `BattleStrategy.act()` is abstract.
- `BattleStrategy.is_valid()` is abstract and returns `bool`.
- `NormalStrategy` works for any Creature and calls `attack()`.
- `AggressiveStrategy` works for transforming Creatures.
- `AggressiveStrategy` calls `transform()`, `attack()`, and `revert()`.
- `DefensiveStrategy` works for healing Creatures.
- `DefensiveStrategy` calls `attack()` and then `heal()`.
- Invalid Creature and strategy combinations return `False` from `is_valid()`.
- Calling `act()` with an invalid combination raises a dedicated exception.
- `tournament.py` creates factories from `ex0` and `ex1`.
- `tournament.py` creates all three strategies.
- A single battle function accepts a list of `(CreatureFactory, BattleStrategy)`.
- Each opponent fights every other opponent once.
- Invalid combinations are caught and reported without a traceback.

Allowed:

- builtins
- standard types
- `abc`
- `typing`
- project imports

Not allowed:

- external libraries
- `eval()`
- `exec()`
- crashing the tournament on an invalid strategy combination

## Commands

```text
cd projects/python07
python3.10 battle.py
python3.10 capacitor.py
python3.10 tournament.py
cd ../..
python3.10 -m compileall -q projects/python07
python3.10 -m flake8 projects/python07
python3.10 -m mypy projects/python07
```

## Gotchas

The official subject is stored as `en.subject.pdf`, with extracted text in
`en.subject.txt`.

Subject source:

- `https://cdn.intra.42.fr/pdf/pdf/203181/en.subject.pdf`

The package `ex0` exposes factories only. The concrete Creature classes stay in
internal modules.

The package `ex1` exposes factories only. Capability and concrete Creature
implementation details stay in internal modules.

Use the factory return type to keep scripts type-safe when calling capability
methods.

The tournament uses base Creatures from each factory, matching the subject
examples.
