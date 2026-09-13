*This project has been created as part of the 42 curriculum by mal-hall, idamadou.*

# A-Maze-ing

## Description

A-Maze-ing reads a configuration file, generates a reproducible maze, writes
its hexadecimal wall representation, and displays it in the terminal. Perfect
mode keeps a single route between cells. Default mode opens extra walls until
the board has multiple routes and at most two ordinary dead ends, making it
suitable for a Pac-Man-like game.

## Instructions

Python 3.10 or later is required.

```sh
make install
make run
make lint
make package
```

The equivalent direct command is:

```sh
python3 a_maze_ing.py config.txt
```

While the terminal menu is active, use its numbered commands to regenerate the
maze, show or hide the shortest path, change wall colour, or save the output.

## Resources and AI usage

- Python documentation for `random`, `collections.deque`, and packaging.
- The 42 subject and supplied `maze_analyzer.py` validation tool.
- Background reading on recursive-backtracking maze generation.

AI was used to review requirements, check the wall-bit logic, find mismatches
between the subject and implementation, and prepare tests. The resulting code
and generated output were checked with flake8, mypy, and the official analyzer.

## Configuration file

The file contains one `KEY=VALUE` pair per line; blank lines and lines beginning
with `#` are ignored.

- `WIDTH`, `HEIGHT`: maze dimensions.
- `ENTRY`, `EXIT`: coordinates in `x,y` form.
- `OUTPUT_FILE`: generated maze file.
- `PERFECT`: `true` for one route, `false` for a playable looping board.
- `SEED`: optional integer, or `random`.
- `INCLUDE_42`: optionally draw the closed-cell 42 pattern.
- `DISPLAY`: must be `terminal`.
- `SHOW_PATH`: initial path visibility.
- `WALL_COLOR`: terminal wall colour.
- `INTERACTIVE`: enable or disable the menu.

## Algorithm choice

An iterative randomized depth-first search first carves a spanning tree. It is
small, deterministic with a seed, and guarantees connectivity. For non-perfect
mazes, additional walls are opened from dead ends until the mandatory playable
board limit is reached. Breadth-first search records a shortest entry-to-exit
solution.

## Reusable module

`mazegen.py` is independent of the command-line and display code. It exposes
one `MazeGenerator` class and is packaged in the root wheel:

```python
from mazegen import MazeGenerator

generator = MazeGenerator(
    width=10,
    height=8,
    entry=(0, 0),
    exit_cell=(9, 7),
    seed=42,
    perfect=False,
).generate()

grid = generator.maze()
path = generator.solution_path()
```

Install it in another environment with `pip install mazegen-*.whl`.

## Team and project management

- mal-hall and idamadou shared implementation, validation, and review.
- Work began with the wall grid and perfect generator, then added output,
  terminal interaction, packaging, and the non-perfect board rules.
- Bit masks and a standalone generator kept the implementation reusable.
- Earlier documentation and the non-perfect flag drifted from the code; the
  final review corrected both and reinforced subject-driven checks.
- Git, Python virtual environments, flake8, mypy, unittest, and the supplied
  analyzer were used.

