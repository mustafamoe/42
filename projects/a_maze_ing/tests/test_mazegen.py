"""Tests for the reusable maze generator."""

from __future__ import annotations

import unittest

from mazegen import EAST
from mazegen import SOUTH
from mazegen import ALL_WALLS
from mazegen import Coord
from mazegen import MazeGenerator


def count_open_edges(generator: MazeGenerator) -> int:
    """Count undirected open edges between non-pattern cells."""
    walls = generator.maze()
    blocked = generator.pattern_cells
    count = 0
    for y in range(generator.height):
        for x in range(generator.width):
            coord = (x, y)
            if coord in blocked:
                continue
            east = (x + 1, y)
            south = (x, y + 1)
            if east[0] < generator.width and east not in blocked:
                if not walls[y][x] & EAST:
                    count += 1
            if south[1] < generator.height and south not in blocked:
                if not walls[y][x] & SOUTH:
                    count += 1
    return count


def follow_path(generator: MazeGenerator) -> list[Coord]:
    """Return path coordinates through the public API."""
    return generator.solution_coordinates()


class MazeGeneratorTests(unittest.TestCase):
    """Exercise generation invariants."""

    def test_perfect_maze_is_spanning_tree(self) -> None:
        """A perfect maze has exactly one fewer edge than open cells."""
        generator = MazeGenerator(14, 10, seed=7, perfect=True).generate()
        open_cells = generator.width * generator.height
        open_cells -= len(generator.pattern_cells)

        self.assertEqual(count_open_edges(generator), open_cells - 1)
        self.assertEqual(follow_path(generator)[0], generator.entry)
        self.assertEqual(follow_path(generator)[-1], generator.exit)

    def test_hex_rows_match_dimensions(self) -> None:
        """Hex output has one digit per cell."""
        generator = MazeGenerator(12, 8, seed=42).generate()
        rows = generator.to_hex_rows()

        self.assertEqual(len(rows), 8)
        self.assertTrue(all(len(row) == 12 for row in rows))
        self.assertTrue(all(char in "0123456789ABCDEF" for row in rows
                            for char in row))

    def test_pattern_cells_are_fully_closed(self) -> None:
        """Every 42 pattern cell keeps all four walls."""
        generator = MazeGenerator(16, 10, seed=21).generate()

        self.assertTrue(generator.pattern_cells)
        for coord in generator.pattern_cells:
            self.assertEqual(generator.cell_value(coord), ALL_WALLS)

    def test_small_maze_omits_pattern_with_warning(self) -> None:
        """Small mazes still generate but report that 42 was omitted."""
        generator = MazeGenerator(5, 5, seed=3).generate()

        self.assertFalse(generator.pattern_cells)
        self.assertTrue(
            any("too small" in item for item in generator.warnings)
        )
        self.assertTrue(generator.solution_path())

    def test_non_perfect_maze_has_no_3x3_open_area(self) -> None:
        """Looped mazes keep the no 3x3 open-room rule."""
        generator = MazeGenerator(
            18,
            12,
            seed=99,
            perfect=False,
            extra_openings=1.0,
        ).generate()

        self.assertFalse(generator._has_open_area_3x3())


if __name__ == "__main__":
    unittest.main()
