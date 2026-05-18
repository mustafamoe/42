# Python Module 02 Notes

## Big idea

This module is about exception handling.

An exception is a problem that happens while the program is running. Instead of letting
the program crash, we can catch the problem and decide what to do.

## Useful keywords

`try` runs code that might fail.

`except` handles the error if something fails.

`raise` creates an error on purpose.

`finally` always runs, even if an error happened.

## Exercise 0: First Exception

File: `ex0/ft_first_exception.py`

Idea:

Convert a string temperature into an integer.

```python
int("25")
```

This works.

```python
int("abc")
```

This fails because `"abc"` is not a number.

The exercise teaches:

- Put risky code inside `try`
- Catch the error with `except`
- Keep the program running after the error

Important lesson:

Use `try` / `except` when input might be invalid.

## Exercise 1: Raising Exceptions

File: `ex1/ft_raise_exception.py`

Idea:

Even if input is a valid number, it can still be wrong for the program.

Examples:

- `"25"` is valid
- `"100"` is a number, but too hot for plants
- `"-50"` is a number, but too cold for plants

The exercise teaches:

- Use `raise` when data breaks your own rule
- Python can raise errors automatically
- You can raise errors manually

Important lesson:

Validation is not only about type. It is also about whether the value makes sense.

## Exercise 2: Different Error Types

File: `ex2/ft_different_errors.py`

Idea:

Different problems create different exception types.

Examples:

```python
int("abc")
```

Raises `ValueError`.

```python
42 / 0
```

Raises `ZeroDivisionError`.

```python
open("/non/existent/file")
```

Raises `FileNotFoundError`.

```python
"plant count: " + 3
```

Raises `TypeError`.

The exercise teaches:

- Catch specific errors with specific `except` blocks
- Give a different response depending on the problem
- Catch multiple error types in one block

Example:

```python
except (ValueError, ZeroDivisionError):
```

Important lesson:

Specific exception types help you understand exactly what went wrong.

## Exercise 3: Custom Errors

File: `ex3/ft_custom_errors.py`

Idea:

Sometimes Python's built-in errors are too general. You can create your own errors for
your own program.

Example:

```python
class GardenError(Exception):
    pass
```

Then you can create more specific errors:

```python
class PlantError(GardenError):
    pass

class WaterError(GardenError):
    pass
```

This creates a family:

```text
Exception
GardenError
PlantError
WaterError
```

The exercise teaches:

- Custom errors make the program easier to understand
- Inheritance lets you group related errors
- Catching `GardenError` also catches `PlantError` and `WaterError`

Important lesson:

Create custom exceptions when your program has its own meaningful error categories.

## Exercise 4: Finally Block

File: `ex4/ft_finally_block.py`

Idea:

Some code must always run, even if there is an error.

Example:

```python
try:
    water_plant("lettuce")
except PlantError:
    print("problem")
finally:
    print("Closing watering system")
```

The `finally` block always runs.

It runs when:

- The code succeeds
- The code fails
- The function returns early

The exercise teaches:

- Use `finally` for cleanup
- Cleanup should happen even after errors
- Resources should not be left open

Important lesson:

Use `finally` for things like closing files, closing connections, or shutting down
systems.

## Module summary

```text
ex0: catch errors
ex1: raise your own errors
ex2: handle different error types
ex3: create custom error types
ex4: always clean up with finally
```

Short version:

This module teaches how to write Python programs that handle problems without crashing.
