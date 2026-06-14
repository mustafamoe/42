"""Terminal rendering for A-Maze-ing."""

from __future__ import annotations

import sys
from pathlib import Path

from mazegen import EAST
from mazegen import NORTH
from mazegen import SOUTH
from mazegen import WEST
from mazegen import Coord
from mazegen import MazeGenerator

RESET = "\033[0m"
COLORS = {
    "plain": "",
    "black": "\033[30m",
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",
}
COLOR_NAMES = tuple(COLORS)


def render_maze(
    generator: MazeGenerator,
    show_path: bool,
    wall_color: str,
) -> str:
    """Render the maze as terminal-friendly ASCII art."""
    color = normalize_color(wall_color)
    path_cells = set(generator.solution_coordinates()) if show_path else set()
    lines: list[str] = []

    for y in range(generator.height):
        top_parts: list[str] = []
        middle_parts: list[str] = []
        for x in range(generator.width):
            coord = (x, y)
            value = generator.cell_value(coord)
            top_parts.append(wall("+", color))
            top_parts.append(wall("---", color) if value & NORTH else "   ")
            middle_parts.append(wall("|", color) if value & WEST else " ")
            middle_parts.append(cell_body(generator, coord, path_cells))
        top_parts.append(wall("+", color))
        last_value = generator.cell_value((generator.width - 1, y))
        middle_parts.append(wall("|", color) if last_value & EAST else " ")
        lines.append("".join(top_parts))
        lines.append("".join(middle_parts))

    bottom_parts: list[str] = []
    for x in range(generator.width):
        value = generator.cell_value((x, generator.height - 1))
        bottom_parts.append(wall("+", color))
        bottom_parts.append(wall("---", color) if value & SOUTH else "   ")
    bottom_parts.append(wall("+", color))
    lines.append("".join(bottom_parts))
    return "\n".join(lines)


def print_result(
    generator: MazeGenerator,
    out_path: Path,
    show_path: bool,
    color: str,
) -> None:
    """Print generation warnings, output location, and visual maze."""
    for warning in generator.warnings:
        print(f"Warning: {warning}", file=sys.stderr)
    print(render_maze(generator, show_path, color))
    print(f"\nOutput: {out_path}")
    print(f"Path: {generator.solution_path()}")


def cell_body(
    generator: MazeGenerator,
    coord: Coord,
    path_cells: set[Coord],
) -> str:
    """Return the three-character body for one visual cell."""
    if coord == generator.entry:
        return " S "
    if coord == generator.exit:
        return " E "
    if generator.is_pattern_cell(coord):
        return " # "
    if coord in path_cells:
        return " . "
    return "   "


def normalize_color(value: str) -> str:
    """Return a supported wall color name."""
    color = value.strip().lower()
    if color not in COLORS:
        names = ", ".join(COLOR_NAMES)
        raise ValueError(f"WALL_COLOR must be one of: {names}")
    return color


def wall(text: str, color: str) -> str:
    """Apply an ANSI color to a wall fragment."""
    if color == "plain":
        return text
    return f"{COLORS[color]}{text}{RESET}"
