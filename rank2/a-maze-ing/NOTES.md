# A-Maze-ing Notes

## Idea

Generate a rectangular maze from a config file, write one hex digit per cell,
show it in the terminal, and expose a reusable `MazeGenerator` module.

## Key concepts

Cell wall bits:

- north: `1`
- east: `2`
- south: `4`
- west: `8`
- fully closed: `F`

The generator starts with every wall closed, then uses randomized depth-first
search to carve a spanning tree through all non-pattern cells.

The carved spanning tree has exactly one path between any two open cells.

The 42 shape is made of fully closed cells. It is omitted with a warning when
the maze is too small or placement would isolate open cells.

## Files

- `a_maze_ing.py`: small command-line entrypoint
- `maze_config.py`: config parsing and generator construction
- `maze_interactive.py`: terminal menu commands
- `maze_output.py`: output file formatting
- `maze_render.py`: terminal ASCII renderer and wall colors
- `mazegen.py`: reusable generator class and maze algorithms
- `visualizer.html`: browser animation of the randomized DFS backtracking
  generator
- `config.txt`: default config using the mandatory `OUTPUT_FILE` key
- `pyproject.toml`: package metadata for `mazegen`
- `tests/test_cli_modules.py`: smoke tests for the split CLI helpers

## Commands

```text
python3.10 a_maze_ing.py config.txt
open visualizer.html
make run
make lint
make test
make package
```

## Interaction

The default `config.txt` sets `INTERACTIVE=true`, so running the program in a
terminal displays a numbered menu after the maze.

Menu actions:

- `1`: generate again using the next seed
- `2`: show or hide the shortest path
- `3`: change maze wall color
- `4`: rewrite the output file
- `0`: exit

Typed aliases also work: `new`, `path`, `color NAME`, `save`, and `quit`.

## Gotchas

Coordinates use `x,y` with `(0,0)` at the top-left corner.

The output metadata uses raw values, not labels:

```text
0,0
19,14
EESS...
```

External borders are always closed.

Pattern cells are excluded from connectivity checks because they are required
to be fully closed.
