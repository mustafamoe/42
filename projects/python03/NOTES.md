# Python Module 03 Notes

## Big idea

This module is about Python collections.

Collections let you store and organize multiple values. Each collection has a different
job:

- `list`: ordered, changeable values
- `tuple`: ordered, fixed values
- `set`: unique values
- `dict`: key-value pairs
- `generator`: values produced one at a time
- comprehension: short syntax to build collections

## Exercise 0: Command Quest

File: `ex0/ft_command_quest.py`

Idea:

Use `sys.argv`, which is a list of command-line arguments.

```python
sys.argv[0]
```

is the program name.

```python
sys.argv[1]
```

is the first real argument.

Important lesson:

Command-line arguments arrive as strings inside a list.

## Exercise 1: Score Analytics

File: `ex1/ft_score_analytics.py`

Idea:

Convert command-line arguments into integer scores and store valid scores in a list.

Invalid values are ignored after printing an error.

Useful list operations:

- `len(scores)` counts values
- `sum(scores)` totals values
- `max(scores)` gets the highest value
- `min(scores)` gets the lowest value

Important lesson:

Lists are good when you need ordered data that can grow.

## Exercise 2: Coordinate System

File: `ex2/ft_coordinate_system.py`

Idea:

Store 3D coordinates as a tuple:

```python
(x, y, z)
```

This type alias:

```python
Coordinate = tuple[float, float, float]
```

means a coordinate is three float values.

Important lesson:

Tuples are good for fixed data that belongs together, like a 3D point.

Gotcha:

Exercise 2 does not authorize `len()`, so the coordinate parser checks the number of
comma-separated values by unpacking them into `x`, `y`, and `z` parts.

## Exercise 3: Achievement Tracker

File: `ex3/ft_achievement_tracker.py`

Idea:

Store player achievements in sets.

Useful set operations:

```python
alice.union(bob)
```

gets achievements from Alice or Bob.

```python
alice.intersection(bob)
```

gets achievements both players have.

```python
alice.difference(bob)
```

gets achievements Alice has and Bob does not have.

Important lesson:

Sets are good for unique values and comparing groups.

## Exercise 4: Inventory System

File: `ex4/ft_inventory_system.py`

Idea:

Store inventory data in a dictionary:

```python
{"sword": 1, "potion": 5}
```

The item name is the key. The quantity is the value.

Useful dictionary operations:

- `dict.keys()` gets all keys
- `dict.values()` gets all values
- `dict.update()` adds or updates values

Important lesson:

Dictionaries are good when one value points to another value.

## Exercise 5: Data Stream

File: `ex5/ft_data_stream.py`

Idea:

Use generators to produce events only when needed.

```python
yield value
```

returns one value and pauses the function.

```python
next(generator)
```

asks for the next value.

Important lesson:

Generators are useful when data should be produced one item at a time instead of stored
all at once.

Gotcha:

Build the 10-event list with a normal loop here. Comprehensions are the main topic of
Exercise 6.

Use `import typing` and `typing.Generator` for the generator type hints, matching the
authorized import style in the subject.

## Exercise 6: Data Alchemist

File: `ex6/ft_data_alchemist.py`

Idea:

Use comprehensions to build collections quickly.

List comprehension:

```python
[player.capitalize() for player in players]
```

Dictionary comprehension:

```python
{player: score for player in players}
```

Comprehension with a filter:

```python
[player for player in players if player == player.capitalize()]
```

Important lesson:

Comprehensions are compact loops used to create new collections.

## Module summary

```text
ex0: command-line arguments as a list
ex1: list processing
ex2: tuples for coordinates
ex3: sets for unique achievements
ex4: dictionaries for inventory
ex5: generators for streams
ex6: comprehensions for transformations
```

Short version:

This module teaches how to choose the right Python collection for the data you have.
