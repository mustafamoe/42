# Python Module 09 Notes

## Big idea

This module practices Pydantic 2.x validation through space-themed data models.

Key concepts:

- `BaseModel` models
- `Field` constraints
- enum-backed string values
- `@model_validator(mode="after")`
- nested Pydantic models
- clean `ValidationError` handling

## Global rules

- Use Python 3.10 or later.
- Use Pydantic 2.x installed with pip.
- Use a virtual environment for local checks.
- Code must pass `flake8`.
- Code must include type annotations and pass `mypy`.
- Avoid deprecated Pydantic v1 decorators such as `@validator`.
- Do not copy helper generator files into the exercise directories.

## Exercise 0: Space Station Data

File:

- `ex0/space_station.py`

Model:

- `SpaceStation`

Important fields:

- station ID, name, crew size, power, oxygen, maintenance date
- optional notes
- operational status defaulting to `True`

## Exercise 1: Alien Contact Logs

File:

- `ex1/alien_contact.py`

Models:

- `ContactType`
- `AlienContact`

Custom rules:

- contact IDs start with `AC`
- physical contacts must be verified
- telepathic contacts need at least 3 witnesses
- strong signals above 7.0 need a received message

## Exercise 2: Space Crew Management

File:

- `ex2/space_crew.py`

Models:

- `Rank`
- `CrewMember`
- `SpaceMission`

Custom rules:

- mission IDs start with `M`
- each mission needs a commander or captain
- missions longer than 365 days need at least 50% experienced crew
- all crew must be active

## Commands

```text
python3.10 -m venv /tmp/python09_venv
/tmp/python09_venv/bin/python -m pip install "pydantic>=2,<3" flake8 mypy

/tmp/python09_venv/bin/python projects/python09/ex0/space_station.py
/tmp/python09_venv/bin/python projects/python09/ex1/alien_contact.py
/tmp/python09_venv/bin/python projects/python09/ex2/space_crew.py

/tmp/python09_venv/bin/python -m compileall -q projects/python09
/tmp/python09_venv/bin/python -m flake8 projects/python09
/tmp/python09_venv/bin/python -m mypy projects/python09
```

## Gotchas

Use `model_validate({...})` in demos when passing raw string timestamps or enum
values. Pydantic validates and converts those values at runtime, while mypy keeps
constructor calls strict.

Subject source:

- `https://cdn.intra.42.fr/pdf/pdf/203184/en.subject.pdf`
