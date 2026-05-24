*This project has been created as part of the 42 curriculum by mal-hall.*

# A-Maze-ing

## Install

```sh
make install
```

## Run

```sh
make run
```

```sh
python3.10 a_maze_ing.py config.txt
```

## Config

```text
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
SEED=42
PERFECT=true
INCLUDE_42=true
EXTRA_OPENINGS=0.12
OUTPUT=maze.txt
SHOW_PATH=true
WALL_COLOR=cyan
INTERACTIVE=false
```

## Output

```text
<hex maze rows>

<entry x,y>
<exit x,y>
<shortest path as N/E/S/W>
```

Wall bits:

```text
north=1 east=2 south=4 west=8
```

## Package

```sh
make package
python3.10 -m pip install mazegen-0.1.0-py3-none-any.whl
```

```python
from mazegen import MazeGenerator

generator = MazeGenerator(20, 15, seed=42).generate()
print(generator.to_hex_rows())
print(generator.solution_path())
```

## Checks

```sh
make lint
make test
```

## Resources

- 42 A-Maze-ing subject
- Python 3.10 documentation

AI was used to review the subject, design tests, and check edge cases.
