# Python Module 00 Notes

## Big idea

This module is about basic Python functions, input, output, variables, conditionals,
loops, and recursion.

Most exercises define a function. The function only runs when it is called.

## Useful basics

`print()` displays text.

`input()` reads text from the user.

`int()` converts text into an integer.

`if`, `elif`, and `else` choose between different paths.

`for` loops repeat work a known number of times.

Recursion means a function calls itself.

## Exercise 0: Hello Garden

File: `ex0/ft_hello_garden.py`

Idea:

Create a function and print a fixed message.

Important lesson:

A function groups code so it can be reused later.

## Exercise 1: Garden Name

File: `ex1/ft_garden_name.py`

Idea:

Read a garden name from the user and print it with formatted output.

```python
name = input("Enter garden name: ")
print(f"Garden: {name}")
```

Important lesson:

Use f-strings when text needs to include variable values.

## Exercise 2: Plot Area

File: `ex2/ft_plot_area.py`

Idea:

Read length and width, convert both values to integers, and multiply them.

```python
length = int(input("Enter length: "))
width = int(input("Enter width: "))
```

Important lesson:

`input()` always returns a string, so numeric input must be converted before doing
math.

## Exercise 3: Harvest Total

File: `ex3/ft_harvest_total.py`

Idea:

Read three harvest values and add them together.

Important lesson:

Store separate input values in variables before combining them.

## Exercise 4: Plant Age

File: `ex4/ft_plant_age.py`

Idea:

Check whether a plant is older than 60 days.

```python
if age > 60:
    print("Plant is ready to harvest!")
else:
    print("Plant needs more time to grow.")
```

Important lesson:

Use conditionals when the program should make a decision.

## Exercise 5: Water Reminder

File: `ex5/ft_water_reminder.py`

Idea:

Check how many days passed since watering.

If the value is greater than 2, print a watering reminder.

Important lesson:

Comparison operators like `>` return `True` or `False`.

## Exercise 6: Count Harvest

Files:

- `ex6/ft_count_harvest_iterative.py`
- `ex6/ft_count_harvest_recursive.py`

Idea:

Print each day until harvest.

Iterative version:

```python
for day in range(1, days + 1):
    print(f"Day {day}")
```

Recursive version:

```python
def print_day(day):
    if day > days:
        return
    print(f"Day {day}")
    print_day(day + 1)
```

Important lesson:

Loops and recursion can solve the same repeated task in different ways.

Gotcha:

`range(1, days + 1)` is used because the end of a range is excluded.

## Exercise 7: Seed Inventory

File: `ex7/ft_seed_inventory.py`

Idea:

Use parameters and conditional branches to print different messages for different
units.

Valid units:

- `packets`
- `grams`
- `area`

Important lesson:

Function parameters let the caller provide values directly.

## Commands

Run an exercise by importing the function and calling it.

Example from the `projects/python00` folder:

```bash
python3 -c 'from ex0.ft_hello_garden import ft_hello_garden; ft_hello_garden()'
```

For exercises that use `input()`, run the same way and then type the requested values.

## Module summary

```text
ex0: print from a function
ex1: read and print user input
ex2: convert input and multiply numbers
ex3: add multiple inputs
ex4: choose with if / else
ex5: compare values
ex6: repeat with loops and recursion
ex7: use parameters and branches
```

Short version:

This module teaches the first building blocks of Python programs.
