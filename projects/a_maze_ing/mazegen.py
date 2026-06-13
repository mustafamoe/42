"""Reusable maze generator for the A-Maze-ing project.

The public API is intentionally small:

```
from mazegen import MazeGenerator

generator = MazeGenerator(20, 15, seed=42).generate()
hex_rows = generator.to_hex_rows()
path = generator.solution_path()
```

Each generated cell is stored as one hexadecimal wall mask:

- north: 1
- east: 2
- south: 4
- west: 8

A value of ``F`` means that all four walls are present.
"""

from __future__ import annotations

from collections import deque
from random import Random

Coord = tuple[int, int]
WallGrid = list[list[int]]

NORTH = 1
EAST = 2
SOUTH = 4
WEST = 8
ALL_WALLS = NORTH | EAST | SOUTH | WEST

DIRECTIONS: dict[str, tuple[int, int, int, int]] = {
    "N": (0, -1, NORTH, SOUTH),
    "E": (1, 0, EAST, WEST),
    "S": (0, 1, SOUTH, NORTH),
    "W": (-1, 0, WEST, EAST),
}

PATTERN_ROWS = (
    "X X XXX",
    "X X   X",
    "XXX XXX",
    "  X X  ",
    "  X XXX",
)


class MazeGenerator:
    """Generate and expose a connected maze with an optional 42 pattern."""

    def __init__(
        self,
        width: int,
        height: int,
        entry: Coord = (0, 0),
        exit_cell: Coord | None = None,
        seed: int | None = None,
        include_pattern: bool = True,
    ) -> None:
        """Store maze parameters and validate their basic shape."""
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = (
            exit_cell
            if exit_cell is not None
            else (width - 1, height - 1)
        )
        self.seed = seed
        self.include_pattern = include_pattern

        self.warnings: list[str] = []
        self.pattern_cells: set[Coord] = set()
        self._walls: WallGrid = []
        self._solution: list[str] = []
        self._generated = False

        self._validate_parameters()

    def generate(self) -> "MazeGenerator":
        """Generate the maze and return this object for chaining."""
        rng = Random(self.seed)
        self.warnings = []
        self.pattern_cells = self._choose_pattern_cells()
        self._walls = [
            [ALL_WALLS for _x in range(self.width)]
            for _y in range(self.height)
        ]

        available = self._available_cells(self.pattern_cells)
        if self.entry not in available or self.exit not in available:
            raise ValueError(
                "entry and exit must not be inside the 42 pattern"
            )

        self._carve_perfect_maze(rng, available)

        self._close_pattern_cells()
        self._close_external_borders()
        self._solution = self._find_shortest_path()
        if not self._solution:
            raise ValueError("entry and exit are not connected")
        self._generated = True
        return self

    def maze(self) -> WallGrid:
        """Return a copy of the generated wall grid."""
        self._require_generated()
        return [row.copy() for row in self._walls]

    def cell_value(self, coord: Coord) -> int:
        """Return one cell's wall mask as an integer."""
        self._require_generated()
        x, y = coord
        if not self._inside(coord):
            raise ValueError("cell coordinate is outside the maze")
        return self._walls[y][x]

    def is_pattern_cell(self, coord: Coord) -> bool:
        """Return whether a coordinate belongs to the closed 42 pattern."""
        return coord in self.pattern_cells

    def to_hex_rows(self) -> list[str]:
        """Return the maze as rows of hexadecimal wall masks."""
        self._require_generated()
        return [
            "".join(format(value, "X") for value in row)
            for row in self._walls
        ]

    def solution_path(self) -> str:
        """Return the shortest entry-to-exit path as N/E/S/W directions."""
        self._require_generated()
        return "".join(self._solution)

    def solution_coordinates(self) -> list[Coord]:
        """Return every coordinate visited by the shortest path."""
        self._require_generated()
        coords = [self.entry]
        current = self.entry
        for step in self._solution:
            dx, dy, _wall, _opposite = DIRECTIONS[step]
            current = (current[0] + dx, current[1] + dy)
            coords.append(current)
        return coords

    def _validate_parameters(self) -> None:
        """Reject invalid maze dimensions and coordinates."""
        if self.width < 2 or self.height < 2:
            raise ValueError("width and height must be at least 2")
        if not self._inside(self.entry):
            raise ValueError("entry coordinate is outside the maze")
        if not self._inside(self.exit):
            raise ValueError("exit coordinate is outside the maze")
        if self.entry == self.exit:
            raise ValueError("entry and exit must be different cells")

    def _choose_pattern_cells(self) -> set[Coord]:
        """Choose a connected-safe placement for the 42 pattern."""
        if not self.include_pattern:
            return set()

        pattern_width = len(PATTERN_ROWS[0])
        pattern_height = len(PATTERN_ROWS)
        if self.width < pattern_width + 2 or self.height < pattern_height + 2:
            self.warnings.append(
                "maze is too small for the 42 pattern; pattern omitted"
            )
            return set()

        max_x = self.width - pattern_width - 1
        max_y = self.height - pattern_height - 1
        candidates = [
            (x, y)
            for y in range(1, max_y + 1)
            for x in range(1, max_x + 1)
        ]
        center_x = (self.width - pattern_width) / 2
        center_y = (self.height - pattern_height) / 2
        candidates.sort(
            key=lambda item: (item[0] - center_x) ** 2
            + (item[1] - center_y) ** 2
        )

        for left, top in candidates:
            cells = self._pattern_cells_at(left, top)
            if self.entry in cells or self.exit in cells:
                continue
            if self._remaining_cells_connected(cells):
                return cells

        self.warnings.append(
            "could not place the 42 pattern without isolating cells"
        )
        return set()

    def _pattern_cells_at(self, left: int, top: int) -> set[Coord]:
        """Return pattern cells at a top-left coordinate."""
        cells: set[Coord] = set()
        for row_index, row in enumerate(PATTERN_ROWS):
            for col_index, marker in enumerate(row):
                if marker == "X":
                    cells.add((left + col_index, top + row_index))
        return cells

    def _available_cells(self, blocked: set[Coord]) -> set[Coord]:
        """Return all non-blocked coordinates."""
        return {
            (x, y)
            for y in range(self.height)
            for x in range(self.width)
            if (x, y) not in blocked
        }

    def _remaining_cells_connected(self, blocked: set[Coord]) -> bool:
        """Return whether all non-blocked cells stay connected."""
        available = self._available_cells(blocked)
        if self.entry not in available or self.exit not in available:
            return False
        visited = {self.entry}
        queue: deque[Coord] = deque([self.entry])
        while queue:
            coord = queue.popleft()
            for neighbor, _name in self._grid_neighbors(coord):
                if neighbor not in available or neighbor in visited:
                    continue
                visited.add(neighbor)
                queue.append(neighbor)
        return len(visited) == len(available)

    def _carve_perfect_maze(
        self,
        rng: Random,
        available: set[Coord],
    ) -> None:
        """Carve a spanning tree through every available cell."""
        start = self.entry
        visited = {start}
        stack = [start]

        while stack:
            current = stack[-1]
            neighbors = [
                (neighbor, name)
                for neighbor, name in self._grid_neighbors(current)
                if neighbor in available and neighbor not in visited
            ]
            if not neighbors:
                stack.pop()
                continue
            neighbor, name = rng.choice(neighbors)
            self._open_wall(current, neighbor, name)
            visited.add(neighbor)
            stack.append(neighbor)

        if len(visited) != len(available):
            raise ValueError("maze parameters create isolated open cells")

    def _grid_neighbors(self, coord: Coord) -> list[tuple[Coord, str]]:
        """Return in-bounds orthogonal neighbors with direction names."""
        result: list[tuple[Coord, str]] = []
        x, y = coord
        for name, (dx, dy, _wall, _opposite) in DIRECTIONS.items():
            neighbor = (x + dx, y + dy)
            if self._inside(neighbor):
                result.append((neighbor, name))
        return result

    def _inside(self, coord: Coord) -> bool:
        """Return whether a coordinate is inside the maze bounds."""
        x, y = coord
        return 0 <= x < self.width and 0 <= y < self.height

    def _open_wall(self, coord: Coord, neighbor: Coord, name: str) -> None:
        """Remove the wall between two adjacent cells."""
        x, y = coord
        nx, ny = neighbor
        _dx, _dy, wall, opposite = DIRECTIONS[name]
        self._walls[y][x] &= ~wall
        self._walls[ny][nx] &= ~opposite

    def _close_pattern_cells(self) -> None:
        """Force every pattern cell and its shared edges closed."""
        for x, y in self.pattern_cells:
            self._walls[y][x] = ALL_WALLS
            for neighbor, name in self._grid_neighbors((x, y)):
                nx, ny = neighbor
                _dx, _dy, wall, opposite = DIRECTIONS[name]
                self._walls[y][x] |= wall
                self._walls[ny][nx] |= opposite

    def _close_external_borders(self) -> None:
        """Ensure outside borders are always walls."""
        for x in range(self.width):
            self._walls[0][x] |= NORTH
            self._walls[self.height - 1][x] |= SOUTH
        for y in range(self.height):
            self._walls[y][0] |= WEST
            self._walls[y][self.width - 1] |= EAST

    def _find_shortest_path(self) -> list[str]:
        """Find a shortest path from entry to exit with BFS."""
        parents: dict[Coord, tuple[Coord, str]] = {}
        visited = {self.entry}
        queue: deque[Coord] = deque([self.entry])

        while queue:
            coord = queue.popleft()
            if coord == self.exit:
                break
            for neighbor, name in self._open_neighbors(coord):
                if neighbor in visited:
                    continue
                visited.add(neighbor)
                parents[neighbor] = (coord, name)
                queue.append(neighbor)

        if self.exit not in visited:
            return []

        path: list[str] = []
        cursor = self.exit
        while cursor != self.entry:
            previous, step = parents[cursor]
            path.append(step)
            cursor = previous
        path.reverse()
        return path

    def _open_neighbors(self, coord: Coord) -> list[tuple[Coord, str]]:
        """Return neighboring cells reachable through open walls."""
        if coord in self.pattern_cells:
            return []

        result: list[tuple[Coord, str]] = []
        x, y = coord
        for name, (dx, dy, wall, _opposite) in DIRECTIONS.items():
            neighbor = (x + dx, y + dy)
            if not self._inside(neighbor):
                continue
            if neighbor in self.pattern_cells:
                continue
            if self._walls[y][x] & wall:
                continue
            result.append((neighbor, name))
        return result

    def _require_generated(self) -> None:
        """Require callers to call generate before reading maze data."""
        if not self._generated:
            raise ValueError("maze has not been generated yet")
