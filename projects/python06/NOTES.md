# Python Module 06 Notes

## Big idea

This module is about Python imports and packages.

The goal is to build one small package and demonstrate:

- package initialization with `__init__.py`
- direct module imports
- package imports
- nested package imports
- absolute imports
- relative imports
- circular import failure
- one way to avoid circular imports

## Global rules

Subject requirements:

- Python 3.10 or later.
- Code must pass `flake8`.
- Code must include type annotations and pass `mypy`.
- Standard classes, collections, and methods are allowed.
- Built-in functions are allowed except `eval()` and `exec()`.
- Only imports of files and modules created in this project are allowed.
- `sys.path` must not be modified.

Authorized imports used here:

- project modules only
- no standard-library imports
- no third-party imports

## Part I: The Alembic

Files:

- `elements.py`
- `alchemy/elements.py`
- `alchemy/__init__.py`
- `ft_alembic_0.py`
- `ft_alembic_1.py`
- `ft_alembic_2.py`
- `ft_alembic_3.py`
- `ft_alembic_4.py`
- `ft_alembic_5.py`

Subject requirements:

- Root `elements.py` defines `create_fire()` and `create_water()`.
- `alchemy/elements.py` defines `create_earth()` and `create_air()`.
- `ft_alembic_0.py` uses `import elements`.
- `ft_alembic_1.py` uses `from elements import ...`.
- `ft_alembic_2.py` uses `import ...` to access `alchemy/elements.py`.
- `ft_alembic_3.py` uses `from ... import ...` to access `alchemy/elements.py`.
- `ft_alembic_4.py` uses `import alchemy`.
- `ft_alembic_4.py` can access `alchemy.create_air()`.
- `ft_alembic_4.py` must show `create_earth()` is not exposed by `alchemy`.
- `ft_alembic_5.py` uses `from alchemy import ...`.

Not allowed:

- exposing every function through `alchemy/__init__.py`
- modifying `sys.path`
- importing external modules

Key point:

`alchemy/__init__.py` is the public package interface. This project exposes
`create_air()` but not `create_earth()` to demonstrate controlled imports.

## Part II: Distillation

Files:

- `alchemy/potions.py`
- `ft_distillation_0.py`
- `ft_distillation_1.py`

Subject requirements:

- `healing_potion()` returns a string using created earth and air elements.
- `strength_potion()` returns a string using created fire and water elements.
- `ft_distillation_0.py` imports from `alchemy.potions` directly.
- `ft_distillation_1.py` uses `import alchemy`.
- `alchemy.heal()` is an alias for `healing_potion()`.
- `alchemy.strength_potion()` is available through the package interface.

Not allowed:

- non-project imports
- changing `sys.path`
- hiding missing package exports by importing from outside the package

Key point:

The package interface can provide friendly aliases while the implementation
stays in a deeper module.

## Part III: The Great Transmutation

Files:

- `alchemy/transmutation/__init__.py`
- `alchemy/transmutation/recipes.py`
- `ft_transmutation_0.py`
- `ft_transmutation_1.py`
- `ft_transmutation_2.py`

Subject requirements:

- `lead_to_gold()` returns the recipe string.
- `recipes.py` must use at least one absolute import and one relative import.
- `ft_transmutation_0.py` imports `alchemy/transmutation/recipes.py` directly.
- `ft_transmutation_1.py` imports the `transmutation` package directly.
- `ft_transmutation_2.py` imports only `alchemy`.

Not allowed:

- using only absolute imports
- using only relative imports
- importing external helpers
- modifying `sys.path`

Key point:

Absolute imports are clear from the project root. Relative imports are useful
inside a package when modules belong together.

## Part IV: Avoid the Explosion

Files:

- `alchemy/grimoire/__init__.py`
- `alchemy/grimoire/light_spellbook.py`
- `alchemy/grimoire/light_validator.py`
- `alchemy/grimoire/dark_spellbook.py`
- `alchemy/grimoire/dark_validator.py`
- `ft_kaboom_0.py`
- `ft_kaboom_1.py`

Subject requirements:

- Light magic validates ingredients without circular import failure.
- Light ingredients are `earth`, `air`, `fire`, and `water`.
- Dark magic intentionally has a circular dependency.
- Dark ingredients are `bats`, `frogs`, `arsenic`, and `eyeball`.
- `ft_kaboom_0.py` records a light spell successfully.
- `ft_kaboom_1.py` imports `dark_spellbook.py` directly and raises an error.

Not allowed:

- using external imports to solve the cycle
- modifying `sys.path`
- making the dark circular import safe

Key point:

The light validator delays the import of `light_spell_allowed_ingredients()`
until validation time. The dark validator imports the spellbook at module load
time, which causes the intended circular import failure.

## Commands

```text
python3.10 projects/python06/ft_alembic_0.py
python3.10 projects/python06/ft_alembic_1.py
python3.10 projects/python06/ft_alembic_2.py
python3.10 projects/python06/ft_alembic_3.py
python3.10 projects/python06/ft_alembic_4.py
python3.10 projects/python06/ft_alembic_5.py
python3.10 projects/python06/ft_distillation_0.py
python3.10 projects/python06/ft_distillation_1.py
python3.10 projects/python06/ft_transmutation_0.py
python3.10 projects/python06/ft_transmutation_1.py
python3.10 projects/python06/ft_transmutation_2.py
python3.10 projects/python06/ft_kaboom_0.py
python3.10 projects/python06/ft_kaboom_1.py
python3.10 -m compileall -q projects/python06
python3.10 -m flake8 projects/python06
python3.10 -m mypy projects/python06
```

Run the scripts from `projects/python06` when checking imports manually:

```text
cd projects/python06
python3.10 ft_alembic_0.py
```

## Expected failures

`ft_alembic_4.py` raises `AttributeError` because `create_earth()` is not
exposed through `alchemy/__init__.py`.

`ft_kaboom_1.py` raises `ImportError` because `dark_spellbook.py` and
`dark_validator.py` import each other at module load time.

Both files still pass `flake8` and `mypy`.

## Gotchas

The official subject is stored as `en.subject.pdf`, with extracted text in
`en.subject.txt`.

Do not add `sys.path` hacks. The scripts are designed to run from the module
directory.

Do not import `typing`, `os`, `sys`, `json`, `csv`, or any other external module.

`alchemy.__init__` should expose only the public package API required by the
exercise.

`INVALID` ends with `VALID`, so validation checks must compare the final status
carefully. This implementation checks for `" - VALID"`.

## Module summary

```text
Part I: simple imports and package interface
Part II: nested module imports and package aliases
Part III: absolute and relative imports together
Part IV: circular import avoidance and intentional circular import failure
```
