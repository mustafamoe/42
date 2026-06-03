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

`PERFECT=true` keeps the spanning tree, so there is exactly one path between
any two open cells.

`PERFECT=false` adds extra openings while rejecting moves that create a fully
open `3x3` area.

The 42 shape is made of fully closed cells. It is omitted with a warning when
the maze is too small or placement would isolate open cells.

## Files

- `a_maze_ing.py`: config parsing, output file, terminal renderer, interaction
- `mazegen.py`: reusable generator class
- `config.txt`: default config using the mandatory `OUTPUT_FILE` key
- `pyproject.toml`: package metadata for `mazegen`
- `tests/test_mazegen.py`: invariant tests

## Commands

```text
python3.10 a_maze_ing.py config.txt
make run
make lint
make test
make package
```

## Interaction

Set `INTERACTIVE=true` in `config.txt`.

Commands:

- `new`: generate again using the next seed
- `path`: show or hide the shortest path
- `color NAME`: change wall color
- `save`: rewrite the output file
- `quit`: exit

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
