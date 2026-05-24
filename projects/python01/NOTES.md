# Python Module 01 Notes

## Subject

Project: Code Cultivation - Object-Oriented Garden Systems

Stored subject files:

- `en.subject.pdf`
- `en.subject.txt`

## General Rules

- Use Python 3.10+.
- Code must pass `flake8`.
- All functions and methods must have type hints and pass `mypy`.
- Each exercise has its own directory and file.
- Use PascalCase for classes and snake_case for functions and variables.
- Do not add input validation unless the subject asks for it.
- Starting from exercise 1, use classes.
- `class`, `def`, and other Python keywords do not need to appear in the
  authorized-function list.
- `if __name__ == "__main__":` is allowed in every exercise for local tests.
- `str.capitalize()` is globally allowed for display if needed.
- Avoid imports and extra helper/built-in functions unless the exercise authorizes
  them or the subject explicitly allows them.

## Key Concepts

- `class` defines a new object type.
- `__init__` initializes object state.
- `self` refers to the current object.
- Methods keep behavior close to the data they update.
- Encapsulation protects state through getters and setters.
- Inheritance lets specialized classes reuse shared parent behavior.
- Nested classes can hold internal components such as statistics.
- `@staticmethod` and `@classmethod` attach behavior to a class in different ways.

## Exercise Checklist

### Exercise 0: Planting Your First Seed

File: `ex0/ft_garden_intro.py`

Allowed:

- `print()`
- `if __name__ == "__main__":`

Do not use:

- Classes.
- Imports.
- Extra helper functions or extra built-in calls.

Requirements:

- Run directly with `python3 ft_garden_intro.py`.
- Store `name`, `height`, and `age` in simple variables.
- Print the plant information.
- Mimic the subject example output.
- Be ready to explain the main guard and shebang.

### Exercise 1: Garden Data Organizer

File: `ex1/ft_garden_data.py`

Allowed:

- `print()`
- Classes and methods.
- `if __name__ == "__main__":`

Do not use:

- Imports.
- `__init__` is not required here; instantiate first, then set attributes.
- Extra helper functions or extra built-in calls.

Requirements:

- Create a `Plant` class.
- Each plant has `name`, `height`, and `age`.
- Instantiate at least three plants.
- Set each plant's attributes to its own values.
- Add `show()` to display plant information.

### Exercise 2: Plant Growth Simulator

File: `ex2/ft_plant_growth.py`

Allowed:

- `print()`
- `range()`
- `round()`
- Classes and methods.
- `if __name__ == "__main__":`

Do not use:

- Imports.
- Extra helper functions or extra built-in calls.

Requirements:

- Reuse/improve the `Plant` class.
- Plants must have `grow()` and `age()` methods.
- Simulate seven days of growth.
- Access class data to calculate and print total weekly growth.
- Different plants may grow differently.

### Exercise 3: Plant Factory

File: `ex3/ft_plant_factory.py`

Allowed:

- `print()`
- `range()`
- `round()`
- Classes and methods.
- `if __name__ == "__main__":`

Do not use:

- Imports.
- Extra helper functions or extra built-in calls.

Requirements:

- Create plants directly with initial name, starting height, and starting age.
- Plants must be ready to use immediately after construction.
- Create at least five different plants.
- Display all plants in an organized format.
- Keep `show()` reusable.

### Exercise 4: Garden Security System

File: `ex4/ft_garden_security.py`

Allowed:

- `print()`
- `range()`
- `round()`
- Classes and methods.
- `if __name__ == "__main__":`

Do not use:

- Imports.
- Name-mangled private attributes with double underscores.
- Extra helper functions or extra built-in calls.

Requirements:

- Protect plant data from corruption.
- Use protected-convention attributes such as `_height` and `_age`.
- Provide `set_height()` and `set_age()`.
- Provide `get_height()` and `get_age()`.
- Reject negative height and age values.
- Print class-level error messages for invalid values.
- Leave existing data unchanged or keep constructor defaults for invalid values.

### Exercise 5: Specialized Plant Types

File: `ex5/ft_plant_types.py`

Allowed:

- `super()`
- `print()`
- `range()`
- `round()`
- Classes and methods.
- `if __name__ == "__main__":`

Do not use:

- Imports.
- Duplicate common plant code in specialized classes.
- Add validation for the new specialized attributes.
- Extra helper functions or extra built-in calls.

Requirements:

- Start from the secured `Plant` class.
- Create `Flower`, `Tree`, and `Vegetable`.
- Each specialized class inherits basic plant features.
- `Flower` has `color` and `bloom()`.
- `Tree` has `trunk_diameter` and `produce_shade()`.
- `Vegetable` has `harvest_season` and `nutritional_value`.
- Use `super()` from specialized classes.
- Override `show()` while reusing parent output.
- Create at least one instance of each specialized type.
- Make the flower bloom.
- Vegetable nutritional value starts at 0 and increases during the grow/age demo.

### Exercise 6: Garden Analytics

File: `ex6/ft_garden_analytics.py`

Allowed:

- `super()`
- `print()`
- `range()`
- `round()`
- `staticmethod()`
- `classmethod()`
- Decorator syntax for static/class methods.
- Classes, nested classes, methods, and one standalone statistics function.
- `if __name__ == "__main__":`

Do not use:

- Imports.
- External statistics helpers.
- Extra helper functions or extra built-in calls beyond the required standalone
  statistics display function.

Requirements:

- Add a static method on `Plant` that checks whether a given age is older than a
  year.
- Add a class method that creates an anonymous plant.
- Create `Seed` inheriting from `Flower`.
- `Seed` holds the number of seeds once the flower has bloomed.
- Improve `Seed.show()`.
- Every `Plant` owns a nested, encapsulated statistics class.
- Track `grow()`, `age()`, and `show()` calls.
- Trees also track `produce_shade()` calls.
- Add one standalone function that displays statistics for any plant type.

## Commands

Run a file:

```sh
cd projects/python01/ex2
python3.10 ft_plant_growth.py
```

Run checks from the repository root:

```sh
python3.10 -m flake8 projects/python01
python3.10 -m mypy projects/python01
```

## Gotchas

- Exercise 0 is the only non-OOP exercise.
- The main guard is allowed even when it is not listed in each exercise.
- Protected attributes use one underscore, not double underscore mangling.
- In exercise 6, `Tree` must receive a `Tree.Stats` object so shade calls can be
  tracked.
- The subject examples are display guides; the subject says exercise 0 has no
  strict output check.
