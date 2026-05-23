# Python Module 01 Notes

## Big idea

This module is about object-oriented programming in Python.

Objects keep data and behavior together. A class describes what an object has and what
it can do.

## Useful basics

`class` creates a new type.

`__init__` runs when a new object is created.

`self` means the current object.

Methods are functions that belong to a class.

Attributes store object data.

Inheritance lets one class reuse and extend another class.

## Exercise 0: Garden Intro

File: `ex0/ft_garden_intro.py`

Idea:

Create simple variables and print them when the file is run directly.

```python
if __name__ == "__main__":
```

means the code runs only when this file is the main program.

Important lesson:

Variables can describe one object, but classes become useful when there are many
similar objects.

## Exercise 1: Garden Data

File: `ex1/ft_garden_data.py`

Idea:

Create a `Plant` class with attributes and a `show()` method.

```python
rose = Plant()
rose.name = "Rose"
rose.height = 25
rose.age = 30
```

Important lesson:

An object can store related data in one place.

## Exercise 2: Plant Growth

File: `ex2/ft_plant_growth.py`

Idea:

Use `__init__` to initialize a plant with name, height, age, and daily growth.

Methods:

- `show()` prints the plant state
- `grow()` increases height
- `age()` increases age by one day

Important lesson:

Methods can change the state stored inside an object.

## Exercise 3: Plant Factory

File: `ex3/ft_plant_factory.py`

Idea:

Create a list of `Plant` objects and loop over them.

```python
plants = [
    Plant("Rose", 25.0, 30),
    Plant("Oak", 200.0, 365),
]
```

Important lesson:

A list can store many objects of the same class.

## Exercise 4: Garden Security

File: `ex4/ft_garden_security.py`

Idea:

Protect plant data with setter methods.

```python
def set_height(self, height: float) -> bool:
    if height < 0:
        return False
    self._height = height
    return True
```

Important lesson:

Setters are useful when values must be checked before changing object state.

Gotcha:

The underscore in `_height` and `_age` means "internal use" by convention. Python does
not make the attribute truly private.

## Exercise 5: Plant Types

File: `ex5/ft_plant_types.py`

Idea:

Use inheritance to create specialized plant types.

Class family:

```text
Plant
Flower
Tree
Vegetable
```

Important features:

- `Flower` adds color and blooming
- `Tree` adds trunk diameter and shade
- `Vegetable` adds harvest season and nutritional value

Important lesson:

Subclasses reuse common behavior from the parent class and add their own behavior.

## Exercise 6: Garden Analytics

File: `ex6/ft_garden_analytics.py`

Idea:

Add statistics and more class features.

Important features:

- nested `Stats` class tracks method calls
- `@staticmethod` checks an age without needing an object
- `@classmethod` creates an anonymous plant
- `Tree.Stats` extends `Plant.Stats`
- `Seed` extends `Flower`

Important lesson:

Classes can be composed, extended, and customized while keeping shared behavior in one
parent class.

## Commands

Run a complete exercise file directly:

```bash
python3 ex2/ft_plant_growth.py
```

Run from the `projects/python01` folder so imports and paths stay simple.

## Module summary

```text
ex0: variables and main guard
ex1: basic class and object attributes
ex2: constructor and methods
ex3: list of objects
ex4: validation with getters and setters
ex5: inheritance and method overriding
ex6: static methods, class methods, nested classes, and statistics
```

Short version:

This module teaches how to model data and behavior with Python classes.
