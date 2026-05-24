# Python Module 03 Notes

## Project Idea

Data Quest introduces Python collections through small game-data scripts:
lists, tuples, sets, dictionaries, generators, and comprehensions.

Subject stored locally:

- `en.subject.pdf`
- `en.subject.txt`

## Global Rules

- Use Python 3.10 or later.
- Pass `flake8`.
- Pass `mypy`.
- Type-hint all functions and methods.
- Handle exceptions gracefully.
- No runtime file I/O in submitted scripts.
- Process data in memory, from command-line arguments, or from `input()`.
- Standard `str`, `int`, and `float` types are allowed with their constructors and
  methods.
- Once a collection type is introduced, its methods and constructor are allowed.

## Exercise 0: Command Quest

File: `ex0/ft_command_quest.py`

Goal: inspect `sys.argv` and print the program name, arguments, and total count.

Authorized:

- `import sys`
- `sys.argv`
- `len()`
- `print()`

Not allowed / avoid:

- Extra imports.
- Runtime file I/O.
- Crashing when no arguments are provided.

## Exercise 1: Score Cruncher

File: `ex1/ft_score_analytics.py`

Goal: parse score arguments into a list, discard invalid values with messages, and
print count, total, average, max, min, and range.

Authorized:

- `import sys`
- `sys.argv`
- `len()`
- `sum()`
- `max()`
- `min()`
- `print()`

Not allowed / avoid:

- Extra imports.
- Runtime file I/O.
- Stopping because one argument is invalid.
- Calling `max()` or `min()` when no valid scores remain.

## Exercise 2: Position Tracker

File: `ex2/ft_coordinate_system.py`

Goal: read valid `x,y,z` coordinates, store them as tuples, display coordinates, and
calculate distances with the 3D Euclidean formula.

Authorized:

- `import math`
- `math.sqrt()`
- `input()`
- `round()`
- `print()`

Not allowed / avoid:

- Extra imports.
- Runtime file I/O.
- Returning until the input is valid.
- Mutable coordinate storage for the final position value.

## Exercise 3: Achievement Hunter

File: `ex3/ft_achievement_tracker.py`

Goal: generate random achievement sets for at least four players, then show all
distinct achievements, achievements shared by all players, achievements unique to
each player, and achievements each player is missing.

Authorized:

- `len()`
- `print()`
- `import random`
- `random.*`
- `set()`
- `set.union()`
- `set.intersection()`
- `set.difference()`

Not allowed / avoid:

- Extra imports.
- Runtime file I/O.
- Duplicate achievement storage for player collections.

## Exercise 4: Inventory Master

File: `ex4/ft_inventory_system.py`

Goal: parse `<item_name>:<quantity>` arguments into a dictionary, reject invalid or
duplicate entries, print item summaries and percentages, report most and least
abundant items, then add one new item with `dict.update()`.

Authorized:

- `import sys`
- `sys.argv`
- `len()`
- `print()`
- `sum()`
- `list()`
- `round()`
- `dict.keys()`
- `dict.values()`
- `dict.update()`

Not allowed / avoid:

- Extra imports.
- Runtime file I/O.
- Accepting invalid syntax.
- Accepting duplicate item names.
- Crashing on non-integer quantities.
- Losing original command-line order when resolving ties.

## Exercise 5: Stream Wizard

File: `ex5/ft_data_stream.py`

Goal: create an endless event generator, print 1000 generated events, build a list of
10 event tuples, and consume that list through a generator used directly in a
`for .. in ..` loop.

Authorized:

- `next()`
- `range()`
- `len()`
- `print()`
- `import typing`
- `typing.Generator`
- `import random`
- `random.*`

Not allowed / avoid:

- Extra imports.
- Runtime file I/O.
- Precomputing the endless stream.
- Consuming the ten-event list without `yield`.

## Exercise 6: Data Alchemist

File: `ex6/ft_data_alchemist.py`

Goal: use list comprehensions to capitalize and filter player names, then use
dictionary comprehensions to create random scores and filter scores above average.

Authorized:

- `import random`
- `random.*`
- `print()`
- `len()`
- `sum()`
- `round()`

Not allowed / avoid:

- Extra imports.
- Runtime file I/O.
- Replacing required comprehensions with normal loops.
- Splitting comprehensions across lines unless line length requires it.

## Commands

```bash
python3.10 -m flake8 projects/python03
python3.10 -m mypy projects/python03
```
