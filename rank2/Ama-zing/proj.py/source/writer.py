"""Output writer for the A-Maze-ing project.

Writes the maze grid in hexadecimal format plus the solution path
to a text file, following the subject's required output format.

Output format:
    - One hex character per cell, one row per line.
    - An empty line separator.
    - Entry coordinates.
    - Exit coordinates.
    - Shortest path as N/E/S/W letters.

Usage:
    from src.output_writer import write_output

    write_output("maze.txt", hex_rows, (0, 0), (19, 14), "SSSEE...")
"""

from __future__ import annotations

# Type alias for a coordinate (x, y)
Coord = tuple[int, int]


def write_output(
    file_path: str,
    hex_rows: list[str],
    entry: Coord,
    exit_: Coord,
    solution: str,
) -> None:
    """Write the maze and solution to a file.

    The file contains:
        - The hex grid (one row per line).
        - An empty line.
        - Entry coordinates as 'x,y'.
        - Exit coordinates as 'x,y'.
        - The shortest path as a string of N/E/S/W letters.

    Args:
        file_path: Path to the output file.
        hex_rows:  List of hex strings, one per maze row.
        entry:     (x, y) entrance coordinate.
        exit_:     (x, y) exit coordinate.
        solution:  Shortest path string e.g. 'SSSEEENNN'.

    Raises:
        OSError: If the file cannot be written.
    """
    with open(file_path, "w") as f:
        # Write the hex grid — one row per line
        for row in hex_rows:
            f.write(row + "\n")

        # Empty line separator (required by subject)
        f.write("\n")

        # Entry, exit, and solution path
        f.write(f"{entry[0]},{entry[1]}\n")
        f.write(f"{exit_[0]},{exit_[1]}\n")
        f.write(solution + "\n")