# Python Module 08 Notes

## Big idea

This module is about real-world Python project environments.

The goal is to practice:

- virtual environment detection
- pip and Poetry dependency files
- optional dependency checks
- numpy-generated data
- pandas analysis
- matplotlib output
- `.env` configuration with `python-dotenv`

## Global rules

Subject requirements:

- Python 3.10 or later.
- Code must pass `flake8`.
- Code must include type annotations and pass `mypy`.
- Exception handling should protect data streams.
- Standard classes, collections, methods, and built-ins are authorized.
- Test with and without virtual environments and dependencies.

## Exercise 0: Entering the Matrix

Files:

- `ex0/construct.py`

Subject requirements:

- Detect whether the program runs inside a virtual environment.
- Display current Python environment information.
- Explain how to create and activate a virtual environment when outside one.
- Show the difference between global and virtual package locations.
- Do not submit a virtual environment.

Allowed:

- `sys`
- `os`
- `site`
- `print()`

Not allowed:

- external libraries
- submitting `matrix_env/`
- unrelated modules

## Exercise 1: Loading Programs

Files:

- `ex1/loading.py`
- `ex1/requirements.txt`
- `ex1/pyproject.toml`

Subject requirements:

- Use `numpy` to generate the simulated Matrix dataset.
- Do not hardcode dataset lists or use `range()` as the dataset source.
- Use `pandas` for data manipulation.
- Use `matplotlib` for visualization.
- Include dependency files for pip and Poetry.
- Detect missing dependencies and show helpful install instructions.
- Include a version comparison function for installed packages.
- Show the pip versus Poetry difference in program output.

Allowed:

- `pandas`
- `requests` when fetching external API data, not used here
- `matplotlib`
- `numpy`
- `sys`
- `importlib`

Not allowed:

- hardcoded Matrix dataset values
- `range()` as the data source
- crashing with a traceback when dependencies are missing
- unrelated modules

## Exercise 2: Accessing the Mainframe

Files:

- `ex2/oracle.py`
- `ex2/.env.example`
- `ex2/.gitignore`

Subject requirements:

- Use `python-dotenv` to load `.env` files.
- Load configuration from environment variables.
- Demonstrate development versus production behavior in output.
- Handle missing configuration with warnings and safe defaults.
- Support `MATRIX_MODE`, `DATABASE_URL`, `API_KEY`, `LOG_LEVEL`,
  and `ZION_ENDPOINT`.
- Keep real secrets out of version control.
- Ensure `.env` is ignored.

Allowed:

- `os`
- `sys`
- `python-dotenv`
- file operations

Not allowed:

- real secrets in the repository
- committing `.env`
- custom `.env` parsing
- unrelated modules

## Commands

```text
cd projects/python08/ex0
python3.10 construct.py

cd ../ex1
python3.10 loading.py
python3.10 -m pip install -r requirements.txt
python3.10 loading.py
poetry install
poetry run python loading.py

cd ../ex2
python3.10 oracle.py
cp .env.example .env
python3.10 oracle.py
MATRIX_MODE=production API_KEY=secret123 python3.10 oracle.py

cd ../../..
python3.10 -m compileall -q projects/python08
python3.10 -m flake8 projects/python08
python3.10 -m mypy projects/python08
```

## Gotchas

The official subject is stored as `en.subject.pdf`, with extracted text in
`en.subject.txt`.

Subject source:

- `https://cdn.intra.42.fr/pdf/pdf/203182/en.subject.pdf`

`loading.py` imports third-party packages dynamically so missing dependencies produce
clear installation output instead of import tracebacks.

`oracle.py` uses `python-dotenv` when available and never parses `.env` manually.
Environment variables override `.env` values because `load_dotenv(..., override=False)`
is used.
