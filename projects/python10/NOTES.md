# Python Module 10 Notes

## Big idea

This module practices functional programming patterns through FuncMage exercises.

Key concepts:

- lambda expressions with `map`, `filter`, `sorted`, `max`, and `min`
- higher-order functions that accept and return callables
- closures with persistent private state
- `functools.reduce`, `functools.partial`, `lru_cache`, and `singledispatch`
- decorators, `functools.wraps`, and `@staticmethod`

## Global rules

Subject requirements:

- Use Python 3.10 or later.
- Code must pass `flake8`.
- Use type hints for all function signatures and return types.
- Use `collections.abc.Callable` when annotating callables.
- External libraries are forbidden.
- File I/O operations are forbidden inside the exercises.
- `eval()` and `exec()` are forbidden.
- Global variables are forbidden.
- Keep the implementation focused on functional programming patterns.

## Exercise 0: Lambda Sanctum

File:

- `ex0/lambda_spells.py`

Required functions:

- `artifact_sorter(artifacts)`
- `power_filter(mages, min_power)`
- `spell_transformer(spells)`
- `mage_stats(mages)`

Authorized focus:

- `map`, `filter`, `sorted`, `min`, `max`, `round`, `sum`, `len`
- lambda expressions for transformations

## Exercise 1: Higher Realm

File:

- `ex1/higher_magic.py`

Required functions:

- `spell_combiner(spell1, spell2)`
- `power_amplifier(base_spell, multiplier)`
- `conditional_caster(condition, spell)`
- `spell_sequence(spells)`

Authorized focus:

- `callable()`
- `collections.abc.Callable`

## Exercise 2: Memory Depths

File:

- `ex2/scope_mysteries.py`

Required functions:

- `mage_counter()`
- `spell_accumulator(initial_power)`
- `enchantment_factory(enchantment_type)`
- `memory_vault()`

Authorized focus:

- closures
- `nonlocal`
- independent private state without globals

## Exercise 3: Ancient Library

File:

- `ex3/functools_artifacts.py`

Required functions:

- `spell_reducer(spells, operation)`
- `partial_enchanter(base_enchantment)`
- `memoized_fibonacci(n)`
- `spell_dispatcher()`

Authorized focus:

- `functools`
- `operator`

## Exercise 4: Master's Tower

File:

- `ex4/decorator_mastery.py`

Required functions and class:

- `spell_timer(func)`
- `power_validator(min_power)`
- `retry_spell(max_attempts)`
- `MageGuild.validate_mage_name(name)`
- `MageGuild.cast_spell(spell_name, power)`

Authorized focus:

- `functools.wraps`
- `@staticmethod`
- `time.sleep` for demo timing

## Commands

```text
/opt/homebrew/bin/python3.10 projects/python10/ex0/lambda_spells.py
/opt/homebrew/bin/python3.10 projects/python10/ex1/higher_magic.py
/opt/homebrew/bin/python3.10 projects/python10/ex2/scope_mysteries.py
/opt/homebrew/bin/python3.10 projects/python10/ex3/functools_artifacts.py
/opt/homebrew/bin/python3.10 projects/python10/ex4/decorator_mastery.py

/opt/homebrew/bin/python3.10 -m compileall -q projects/python10
/opt/homebrew/bin/python3.10 -m flake8 projects/python10
/opt/homebrew/bin/python3.10 -m mypy projects/python10
```

## Gotchas

Do not add helper-generated data or attachment scripts to the submitted exercise
directories. The helper is useful for manual testing, but the subject only asks for the
five exercise files.

Subject source:

- `https://cdn.intra.42.fr/pdf/pdf/205818/en.subject.pdf`
