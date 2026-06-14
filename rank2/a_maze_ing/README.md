*This project has been created as part of the 42 curriculum by <*mal-hall*>, <*idamadou*>.*

# A-Maze-ing

## Description

A-Maze-ing is a Python maze generator and terminal renderer. It reads a config file, generates a connected maze, writes the maze as hexadecimal wall masks, and can print the shortest path from entry to exit.

The maze uses bitmasks for walls:

* North: `1`
* East: `2`
* South: `4`
* West: `8`

## Installation

Python 3.10 or newer is required. Optional development tools can be installed with:

```bash
make install
```

## Execution

Run with the provided config file:

```bash
python3 a_maze_ing.py config.txt
```

Or through the Makefile:

```bash
make run
```

## Config File Structure

The configuration file uses one `KEY=VALUE` pair per line. Lines starting with `#` are comments.

Mandatory keys:

* `WIDTH`: maze width in cells.
* `HEIGHT`: maze height in cells.
* `ENTRY`: start coordinate as `x,y`.
* `EXIT`: exit coordinate as `x,y`.
* `OUTPUT_FILE`: output file path.
* `PERFECT`: `true` for exactly one path from entry to exit, `false` to open one extra wall and allow a loop.

Optional keys:

* `SEED`: integer seed for reproducible mazes, or `random`.
* `INCLUDE_42`: `true` to draw the `42` pattern with closed cells when the maze is large enough.
* `DISPLAY`: only `terminal` is supported.
* `SHOW_PATH`: `true` to show the shortest path in the terminal output.
* `WALL_COLOR`: one of `plain`, `black`, `red`, `green`, `yellow`, `blue`, `magenta`, `cyan`, or `white`.
* `INTERACTIVE`: `true` to show the terminal menu when stdin is interactive.

## Maze Generation Algorithm

The generator uses randomized depth-first search with a stack, often called recursive backtracking.

It starts with all walls closed. Each time it moves to an unvisited neighbor, it removes the wall between the current cell and that neighbor. If a cell has no unvisited neighbors, the stack backtracks to an earlier cell.

For `PERFECT=true`, this creates a spanning tree, so there is exactly one path between any two open cells. For `PERFECT=false`, the generator opens one extra wall after the perfect maze is carved, creating at least one loop.

## Reusable Code

The reusable generator lives in `mazegen.py`. It can be imported directly or installed from the built `mazegen-0.1.0-py3-none-any.whl` package.

Example:

```python
from mazegen import EAST
from mazegen import MazeGenerator

generator = MazeGenerator(width=10, height=10, seed=42).generate()

rows = generator.to_hex_rows()
path = generator.solution_path()
coords = generator.solution_coordinates()

if generator.cell_value((0, 0)) & EAST:
    print("East wall is closed at 0,0")

print(rows)
print(path)
print(coords)
```

## Project Files

* `a_maze_ing.py`: command-line entrypoint.
* `maze_config.py`: config loading and validation.
* `maze_output.py`: output file writer.
* `maze_render.py`: terminal ASCII renderer.
* `maze_interactive.py`: optional terminal menu.
* `mazegen.py`: reusable maze generator.
* `visualizer.html`: browser visualization of the backtracking algorithm.

## Features

* Reproducible random generation with `SEED`.
* Perfect and non-perfect maze modes through `PERFECT`.
* Shortest path output.
* Terminal rendering with optional path display and wall colors.
* Optional visible `42` pattern using fully closed cells.
* Installable `mazegen` package files.

## Resources

* **Recursive Backtracking**: [Wikipedia - Maze generation algorithms](https://en.wikipedia.org/wiki/Maze_generation_algorithm#Recursive_backtracker)

## Team and Project Management

* **Roles**: *mal-hall / idamadou* co-developed the maze generator, bitmask representation, terminal rendering, config handling, and packaging.
* **Planning**: The project moved from a simple script toward smaller modules so the generator could be reused later.
* **What worked well**: Bitmask walls kept the maze structure compact and easy to export as hexadecimal digits.
* **What could be improved**: More automated tests could be added around config parsing, maze validity, and output formatting.
* **Tools used**: Python, `Makefile`, `flake8`, `mypy`, and AI assistance during debugging and refactoring.
