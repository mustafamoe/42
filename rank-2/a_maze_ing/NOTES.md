# A-Maze-ing notes

Subject v2.3 is stored in `resources/en.subject.pdf`; its extracted text and
the official `maze_analyzer.py` and `mlx-2.2.tgz` are resources only.

The generator first carves a randomized depth-first spanning tree. With
`PERFECT=false`, it opens extra walls until no more than two real dead ends
remain; with `PERFECT=true`, it leaves the tree unchanged. BFS records the
shortest path. The terminal menu provides regeneration, path visibility, and
wall-colour controls.

Exact submission:

```text
.gitignore  LICENSE.md  Makefile  README.md  a_maze_ing.py  config.txt
maze_config.py  maze_interactive.py  maze_output.py  maze_render.py
mazegen.py  pyproject.toml  mazegen-0.1.0-py3-none-any.whl
```

Private unit tests and the older validator are in `tests/`. The current review
fixed non-perfect generation, added the required licence, corrected the README,
and rebuilt the reusable wheel from `mazegen.py` only.

Validation: Python 3.10, flake8, required mypy flags, unittest, package rebuild,
fresh-environment wheel import, and the official analyzer in both generation
modes. Default mode reports multiple loops and at most two real dead ends;
perfect mode reports zero loops.

