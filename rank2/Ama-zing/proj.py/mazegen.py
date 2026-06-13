"""Maze generator for the A-Maze-ing project.

Uses the recursive backtracker (DFS) algorithm.

Each cell stores its walls as a single integer using bit flags:
    NORTH = 1  (bit 0)
    EAST  = 2  (bit 1)
    SOUTH = 4  (bit 2)
    WEST  = 8  (bit 3)

A wall being set (1) means CLOSED. 0 means OPEN.

Usage:
    from mazegen.generator import MazeGenerator

    gen = MazeGenerator(width=20, height=15, seed=42, perfect=True)
    gen.generate()

    hex_rows = gen.to_hex_rows()   # list of strings, one per row
    path     = gen.solution_path() # e.g. "SSSEEENNN..."
"""

from __future__ import annotations

from collections import deque
from random import Random
from typing import Optional

# Wall bit flags — each wall is one bit in the cell's integer value
NORTH = 1
EAST  = 2
SOUTH = 4
WEST  = 8
ALL_WALLS = NORTH | EAST | SOUTH | WEST

# Maps a direction letter to:
# (col_offset, row_offset, wall_on_current_cell, wall_on_neighbor)
DIRECTIONS: dict[str, tuple[int, int, int, int]] = {
    "N": ( 0, -1, NORTH, SOUTH),
    "E": ( 1,  0, EAST,  WEST),
    "S": ( 0,  1, SOUTH, NORTH),
    "W": (-1,  0, WEST,  EAST),
}

# The "42" pattern — 'X' = fully closed cell, ' ' = normal cell
# 5 rows tall, 7 columns wide
PATTERN_42 = [
    "X X XXX",
    "X X   X",
    "XXX XXX",
    "  X X  ",
    "  X XXX",
]

PATTERN_W = len(PATTERN_42[0])  # 7
PATTERN_H = len(PATTERN_42)     # 5

# Type alias for a coordinate (col, row) = (x, y)
Coord = tuple[int, int]


class MazeGenerator:
    """Generates a maze using the recursive backtracker algorithm.

    Args:
        width:     Number of columns.
        height:    Number of rows.
        entry:     (x, y) of the maze entrance.
        exit_cell: (x, y) of the maze exit. Defaults to bottom-right.
        seed:      Random seed for reproducibility. None = random.
        perfect:   If True, only one path exists between entry and exit.
    """

    def __init__(
        self,
        width: int,
        height: int,
        entry: Coord = (0, 0),
        exit_cell: Optional[Coord] = None,
        seed: Optional[int] = None,
        perfect: bool = True,
    ) -> None:
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit_cell if exit_cell is not None else (width - 1, height - 1)
        self.seed = seed
        self.perfect = perfect

        # Filled in by generate()
        self.grid: list[list[int]] = []
        self.pattern_cells: set[Coord] = set()
        self._solution: list[str] = []

        self._validate()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def generate(self) -> "MazeGenerator":
        """Generate the maze. Returns self for chaining.

        Steps:
            1. Fill grid with all walls closed.
            2. Place "42" pattern at center (or skip if too small and add an error message).
            3. Carve a perfect maze through all non-pattern cells.
            4. If not perfect, knock down some extra walls.
            5. Seal the outer border.
            6. Find the shortest solution path with BFS.
        """
        rng = Random(self.seed)

        # Step 1 — every cell starts fully walled
        self.grid = [
            [ALL_WALLS] * self.width
            for _ in range(self.height)
        ]

        # Step 2 — place "42" pattern (may be empty if maze too small)
        self.pattern_cells = self._place_pattern()

        # Step 3 — carve the maze (DFS skips pattern cells)
        open_cells = self._open_cells()
        self._carve(rng, open_cells)

        # Step 4 — optional: knock down extra walls for imperfect maze
        if not self.perfect:
            self._add_loops(rng, open_cells)

        # Step 5 — lock the outer border and pattern cells
        self._seal_border()
        self._seal_pattern()

        # Step 6 — find the solution
        self._solution = self._bfs()
        if not self._solution:
            raise ValueError("No path between entry and exit. Try a different seed.")

        return self

    def to_hex_rows(self) -> list[str]:
        """Return the maze as a list of hex strings, one per row.

        Each character is one cell's wall bitmask in uppercase hex.
        Example: ["FE9A...", "3C41...", ...]
        """
        self._check_generated()
        return [
            "".join(format(cell, "X") for cell in row)
            for row in self.grid
        ]

    def solution_path(self) -> str:
        """Return the shortest path from entry to exit.

        Each character is a direction: N, E, S, or W.
        Example: "SSSEEENNN"
        """
        self._check_generated()
        return "".join(self._solution)

    def solution_coords(self) -> list[Coord]:
        """Return every (x, y) coordinate along the solution path."""
        self._check_generated()
        coords = [self.entry]
        x, y = self.entry
        for step in self._solution:
            dx, dy, _, _ = DIRECTIONS[step]
            x += dx
            y += dy
            coords.append((x, y))
        return coords

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _validate(self) -> None:
        """Raise ValueError if any parameter is obviously wrong."""
        if self.width < 2 or self.height < 2:
            raise ValueError("Width and height must be at least 2.")
        if not self._in_bounds(self.entry):
            raise ValueError(f"Entry {self.entry} is outside the maze.")
        if not self._in_bounds(self.exit):
            raise ValueError(f"Exit {self.exit} is outside the maze.")
        if self.entry == self.exit:
            raise ValueError("Entry and exit must be different cells.")

    def _in_bounds(self, coord: Coord) -> bool:
        """Return True if coord is inside the grid."""
        x, y = coord
        return 0 <= x < self.width and 0 <= y < self.height

    def _open_cells(self) -> set[Coord]:
        """Return all cells that are NOT part of the pattern."""
        return {
            (x, y)
            for y in range(self.height)
            for x in range(self.width)
            if (x, y) not in self.pattern_cells
        }

    def _neighbors(self, coord: Coord) -> list[tuple[Coord, str]]:
        """Return all in-bounds neighbors of coord with direction labels."""
        x, y = coord
        result = []
        for name, (dx, dy, _, _) in DIRECTIONS.items():
            nb = (x + dx, y + dy)
            if self._in_bounds(nb):
                result.append((nb, name))
        return result

    def _open_wall(self, a: Coord, b: Coord, direction: str) -> None:
        """Remove the wall between cell a and its neighbor b."""
        ax, ay = a
        bx, by = b
        _, _, wall, opposite = DIRECTIONS[direction]
        self.grid[ay][ax] &= ~wall      # clear wall on cell a
        self.grid[by][bx] &= ~opposite  # clear matching wall on cell b

    # ------------------------------------------------------------------
    # Step 3 — DFS maze carving
    # ------------------------------------------------------------------

    def _carve(self, rng: Random, open_cells: set[Coord]) -> None:
        """Carve a perfect maze through open_cells using iterative DFS.

        Starts at entry, visits every open cell exactly once,
        knocking down walls as it goes. Uses a list as a stack
        to avoid Python's recursion limit.
        """
        visited: set[Coord] = {self.entry}
        stack: list[Coord] = [self.entry]

        while stack:
            current = stack[-1]

            # Find neighbors that are open and not yet visited
            unvisited = [
                (nb, name)
                for nb, name in self._neighbors(current)
                if nb in open_cells and nb not in visited
            ]

            if not unvisited:
                stack.pop()  # dead end — backtrack
                continue

            # Pick a random unvisited neighbor and knock down the wall
            nb, direction = rng.choice(unvisited)
            self._open_wall(current, nb, direction)
            visited.add(nb)
            stack.append(nb)

    # ------------------------------------------------------------------
    # Step 4 — Extra openings for imperfect maze
    # ------------------------------------------------------------------

    def _add_loops(self, rng: Random, open_cells: set[Coord], ratio: float = 0.12) -> None:
        """Open extra walls to create loops (makes maze imperfect).

        Skips any opening that would create a 3x3 open area.
        Only looks East and South walls to avoid counting each wall twice.
        """
        candidates = []
        for x, y in open_cells:
            for direction in ("E", "S"):
                dx, dy, wall, _ = DIRECTIONS[direction]
                nb = (x + dx, y + dy)
                if nb in open_cells and self.grid[y][x] & wall:
                    candidates.append(((x, y), nb, direction))

        rng.shuffle(candidates)
        target = max(1, int(len(candidates) * ratio))
        opened = 0

        for coord, nb, direction in candidates:
            if opened >= target:
                break
            self._open_wall(coord, nb, direction)
            if self._has_3x3_open():
                # Undo — this opening made a 3x3 room
                ax, ay = coord
                bx, by = nb
                _, _, wall, opposite = DIRECTIONS[direction]
                self.grid[ay][ax] |= wall
                self.grid[by][bx] |= opposite
            else:
                opened += 1

    def _has_3x3_open(self) -> bool:
        """Return True if any 3x3 block of cells has no internal walls."""
        for top in range(self.height - 2):
            for left in range(self.width - 2):
                # Skip windows that overlap the pattern
                if any(
                    (left + dx, top + dy) in self.pattern_cells
                    for dy in range(3)
                    for dx in range(3)
                ):
                    continue

                # All East walls in the left two columns must be open
                h_open = all(
                    not (self.grid[top + dy][left + dx] & EAST)
                    for dy in range(3)
                    for dx in range(2)
                )
                # All South walls in the top two rows must be open
                v_open = all(
                    not (self.grid[top + dy][left + dx] & SOUTH)
                    for dy in range(2)
                    for dx in range(3)
                )
                if h_open and v_open:
                    return True
        return False

    # ------------------------------------------------------------------
    # Step 2 — "42" pattern placement
    # ------------------------------------------------------------------

    def _place_pattern(self) -> set[Coord]:
        """Place the "42" pattern at the center of the maze.

        Returns the set of cells used, or an empty set if the maze
        is too small to fit the pattern with at least 1 cell margin.
        """
        # Need room for pattern + 1 cell margin on each side
        if self.width < PATTERN_W + 2 or self.height < PATTERN_H + 2:
            print("Warning: maze too small for the '42' pattern; skipping.")
            return set()

        # Place at center
        left = (self.width - PATTERN_W) // 2
        top  = (self.height - PATTERN_H) // 2

        cells: set[Coord] = set()
        for row_i, row in enumerate(PATTERN_42):
            for col_i, ch in enumerate(row):
                if ch == "X":
                    cells.add((left + col_i, top + row_i))

        # Don't block entry or exit
        if self.entry in cells or self.exit in cells:
            print("Warning: '42' pattern overlaps entry/exit; skipping.")
            return set()

        return cells

    # ------------------------------------------------------------------
    # Step 5 — Sealing
    # ------------------------------------------------------------------

    def _seal_border(self) -> None:
        """Close all outer edge walls."""
        for x in range(self.width):
            self.grid[0][x] |= NORTH                  # top row
            self.grid[self.height - 1][x] |= SOUTH    # bottom row
        for y in range(self.height):
            self.grid[y][0] |= WEST                   # left column
            self.grid[y][self.width - 1] |= EAST      # right column

    def _seal_pattern(self) -> None:
        """Close all walls of pattern cells and their shared edges."""
        for x, y in self.pattern_cells:
            self.grid[y][x] = ALL_WALLS
            # Also force the neighbor's shared wall closed
            for nb, direction in self._neighbors((x, y)):
                nx, ny = nb
                _, _, _, opposite = DIRECTIONS[direction]
                self.grid[ny][nx] |= opposite

    # ------------------------------------------------------------------
    # Step 6 — BFS pathfinding
    # ------------------------------------------------------------------

    def _bfs(self) -> list[str]:
        """Find the shortest path from entry to exit using BFS.

        Returns a list of direction letters e.g. ['S', 'S', 'E'].
        Returns an empty list if no path exists.
        """
        parents: dict[Coord, tuple[Coord, str]] = {}
        visited: set[Coord] = {self.entry}
        queue: deque[Coord] = deque([self.entry])

        while queue:
            x, y = queue.popleft()

            if (x, y) == self.exit:
                break

            for direction, (dx, dy, wall, _) in DIRECTIONS.items():
                if self.grid[y][x] & wall:
                    continue  # wall is closed, can't go this way
                nb = (x + dx, y + dy)
                if not self._in_bounds(nb) or nb in self.pattern_cells:
                    continue
                if nb in visited:
                    continue
                visited.add(nb)
                parents[nb] = ((x, y), direction)
                queue.append(nb)

        if self.exit not in visited:
            return []

        # Walk backwards from exit to entry to reconstruct the path
        path: list[str] = []
        cursor = self.exit
        while cursor != self.entry:
            prev, step = parents[cursor]
            path.append(step)
            cursor = prev

        path.reverse()
        return path

    # ------------------------------------------------------------------
    # Guard
    # ------------------------------------------------------------------

    def _check_generated(self) -> None:
        """Raise an error if generate() has not been called yet."""
        if not self.grid:
            raise ValueError("Call generate() before reading maze data.")