*This project has been created as part of the 42 curriculum by \<your_login\>.*

# A-Maze-ing

## Description

A maze generator written in Python that reads a configuration file, generates a maze, and writes it to an output file using a hexadecimal wall representation. The maze can be perfect (single path between entry and exit) or imperfect. A visual representation is provided via terminal ASCII rendering.

The maze generation logic is packaged as a standalone reusable module (`mazegen-*.whl`) that can be installed via pip and imported in other projects.

## Instructions

### Requirements

- Python 3.10 or later
- pip

### Installation

```bash
make install
```

### Running the project

```bash
make run
```

Or manually:

```bash
python3 a_maze_ing.py config.txt
```

### Other Makefile commands

```bash
make debug    # run with pdb debugger
make lint     # run flake8 and mypy
make clean    # remove __pycache__ and .mypy_cache
```

## Configuration File

The configuration file uses `KEY=VALUE` pairs, one per line. Lines starting with `#` are treated as comments and ignored.

### Mandatory keys

| Key | Description | Example |
|---|---|---|
| `WIDTH` | Maze width in cells | `WIDTH=20` |
| `HEIGHT` | Maze height in cells | `HEIGHT=15` |
| `ENTRY` | Entry coordinates (x,y) | `ENTRY=0,0` |
| `EXIT` | Exit coordinates (x,y) | `EXIT=19,14` |
| `OUTPUT_FILE` | Output filename | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | Perfect maze (single path) | `PERFECT=True` |

### Optional keys

| Key | Description | Example |
|---|---|---|
| `SEED` | Random seed for reproducibility | `SEED=42` |

### Example config file

```ini
# Maze configuration
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=42
```

## Maze Generation Algorithm

<!-- TODO: fill in once algorithm is chosen -->

**Algorithm chosen:** Recursive Backtracker (Depth-First Search)

**How it works:**
We have a grid and will start at one box/room. Any room that is reached will get marked as visited. Then, we move to a random neightbor and remove the wall in the process. We keep repeating this until they're all visited and we can't move on. The we just go backwards to the box/room we stared from and stop there. Now we would have exactly one open path that would work and reach the end.

    * uses recursion (a simple stack)

**Why this algorithm:**
<!-- Explain why you chose it — simplicity, perfect maze support, etc. -->

## Reusable Module

The maze generation logic is available as a standalone pip-installable package located at the root of the repository.

**Package name:** `mazegen-1.0.0-py3-none-any.whl`

### Installing the package

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

### Basic usage example

```python
from mazegen import MazeGenerator

# Create a 20x15 perfect maze with a fixed seed
gen = MazeGenerator(width=20, height=15, perfect=True, seed=42)
gen.generate()

# Access the grid
grid = gen.grid  # 2D list of cells

# Access the solution path
path = gen.solve(entry=(0, 0), exit=(19, 14))
print(path)  # e.g. "SSSEEENNE..."
```

### Custom parameters

<!-- TODO: document all parameters once MazeGenerator class is finalized -->

| Parameter | Type | Description |
|---|---|---|
| `width` | int | Number of columns |
| `height` | int | Number of rows |
| `perfect` | bool | If True, single path between entry and exit |
| `seed` | int or None | Random seed for reproducibility |

## Resources

- [Maze generation algorithms — Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Recursive backtracker explanation — Jamis Buck's blog](http://weblog.jamisbuck.org/2010/12/27/maze-generation-recursive-backtracker)
- [Breadth-First Search for pathfinding](https://en.wikipedia.org/wiki/Breadth-first_search)
- [Python typing module docs](https://docs.python.org/3/library/typing.html)
- [flake8 documentation](https://flake8.pycqa.org/)
- [mypy documentation](https://mypy.readthedocs.io/)

**AI usage:** Claude (Anthropic) was used to explain concepts (decorators, algorithms, data structures), review code logic, and answer questions during development. All code was written by the project author.

## Team and Project Management

**Team members:**
- `<your_login>` — <!-- role -->

**Planning:**
<!-- TODO: fill in as project progresses -->
- Week 1: config parser, grid structure, maze generation
- Week 2: output writer, pathfinder, visual display
- Week 3: pip package, README, testing, cleanup

**What went well:**
<!-- Fill in at the end -->

**What could be improved:**
<!-- Fill in at the end -->

**Tools used:**
- VS Code
- Python venv
- pytest
<!-- add more as needed -->