"""Output file formatting for A-Maze-ing."""

from __future__ import annotations

from pathlib import Path

from mazegen import Coord
from mazegen import MazeGenerator


def write_output(path: Path, generator: MazeGenerator) -> None:
    """Write hex rows, metadata, and shortest path to a file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = generator.to_hex_rows()
    lines.append("")
    lines.append(format_coord(generator.entry))
    lines.append(format_coord(generator.exit))
    lines.append(generator.solution_path())
    path.write_text("\n".join(lines) + "\n")


def format_coord(coord: Coord) -> str:
    """Format one coordinate as x,y."""
    return f"{coord[0]},{coord[1]}"
