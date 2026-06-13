"""Basic terminal visualizer for the A-Maze-ing project.

Draws the maze using simple ASCII characters.
Lets the user re-generate, toggle the path, and quit.

Controls:
    [p]     Show/hide solution path
    [c]     Change wall color
    [enter] Re-generate a new maze
    [q]     Quit
"""

from __future__ import annotations

import os
import sys

# Wall bit flags — must match generator.py
NORTH = 1
EAST  = 2
SOUTH = 4
WEST  = 8

# A few basic ANSI colors
RESET  = "\033[0m"
RED    = "\033[31m"
GREEN  = "\033[32m"
YELLOW = "\033[33m"
BLUE   = "\033[34m"
CYAN   = "\033[36m"
WHITE  = "\033[37m"

# Wall color options — cycle through these with [c]
WALL_COLORS = [WHITE, CYAN, YELLOW, RED]

# Type alias
Coord = tuple[int, int]


class Visualizer:
    """Draws the maze in the terminal and handles user input.

    Args:
        generator: A MazeGenerator instance after generate() was called.
        entry:     (x, y) entrance coordinate.
        exit_:     (x, y) exit coordinate.
    """

    def __init__(self, generator: object, entry: Coord, exit_: Coord) -> None:
        self._gen = generator
        self._entry = entry
        self._exit = exit_
        self._show_path = False
        self._color_idx = 0

        # Pre-compute which cells are on the solution path
        self._path_set: set[Coord] = set(generator.solution_coords())  # type: ignore

    def run(self) -> None:
        """Start the interactive loop — draw the maze and wait for input."""
        self._draw()

        while True:
            key = _read_key()

            if key in ("q", "Q"):
                print("\nBye!")
                break

            elif key in ("\r", "\n", " "):
                # Re-generate a new maze
                self._gen.generate()  # type: ignore
                self._path_set = set(self._gen.solution_coords())  # type: ignore
                self._show_path = False
                self._draw()

            elif key in ("p", "P"):
                # Toggle path on/off
                self._show_path = not self._show_path
                self._draw()

            elif key in ("c", "C"):
                # Cycle to the next wall color
                self._color_idx = (self._color_idx + 1) % len(WALL_COLORS)
                self._draw()

    def _draw(self) -> None:
        """Clear the screen and draw the full maze."""
        _clear_screen()

        grid = self._gen.grid  # type: ignore
        height = self._gen.height  # type: ignore
        width = self._gen.width  # type: ignore
        wall_color = WALL_COLORS[self._color_idx]

        for row in range(height):

            # -- Top edge of this row of cells --
            top_line = ""
            for col in range(width):
                cell = grid[row][col]
                # Corner post
                top_line += wall_color + "+" + RESET
                # North wall — draw if closed, space if open
                if cell & NORTH:
                    top_line += wall_color + "--" + RESET
                else:
                    top_line += "  "
            # Last corner post
            top_line += wall_color + "+" + RESET
            print(top_line)

            # -- The cell contents row --
            cell_line = ""
            for col in range(width):
                cell = grid[row][col]
                coord = (col, row)

                # West wall
                if cell & WEST:
                    cell_line += wall_color + "|" + RESET
                else:
                    cell_line += " "

                # What to show inside the cell
                cell_line += _cell_content(
                    coord,
                    self._entry,
                    self._exit,
                    self._path_set,
                    self._show_path,
                    self._gen.pattern_cells,  # type: ignore
                )

            # Last east wall of the row
            last_cell = grid[row][width - 1]
            if last_cell & EAST:
                cell_line += wall_color + "|" + RESET
            else:
                cell_line += " "
            print(cell_line)

        # -- Bottom edge of the entire maze --
        bottom = ""
        for col in range(width):
            cell = grid[height - 1][col]
            bottom += wall_color + "+" + RESET
            if cell & SOUTH:
                bottom += wall_color + "--" + RESET
            else:
                bottom += "  "
        bottom += wall_color + "+" + RESET
        print(bottom)

        # Controls reminder
        print()
        print("[p] path  [c] color  [enter] new maze  [q] quit")
        print()


def _cell_content(
    coord: Coord,
    entry: Coord,
    exit_: Coord,
    path_set: set[Coord],
    show_path: bool,
    pattern_cells: set[Coord],
) -> str:
    """Return the two-character string to display inside a cell.

    Args:
        coord:         The cell's (x, y) coordinate.
        entry:         Entrance coordinate.
        exit_:         Exit coordinate.
        path_set:      Set of coordinates on the solution path.
        show_path:     Whether to show the path.
        pattern_cells: Set of cells used by the 42 pattern.

    Returns:
        Two-character colored string.
    """
    if coord == entry:
        return GREEN + "EN" + RESET
    if coord == exit_:
        return YELLOW + "EX" + RESET
    if show_path and coord in path_set:
        return CYAN + "* " + RESET
    if coord in pattern_cells:
        return BLUE + "##" + RESET
    return "  "


def _clear_screen() -> None:
    """Clear the terminal screen."""
    os.system("clear" if os.name != "nt" else "cls")


def _read_key() -> str:
    """Read a single keypress without needing to press Enter.

    Falls back to normal input() if the terminal doesn't support it.

    Returns:
        A single character string.
    """
    try:
        import tty
        import termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            key = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return key
    except Exception:
        return input("command: ").strip()[:1] or "\r"


def render_static(
    generator: object,
    entry: Coord,
    exit_: Coord,
    solution: str = "",
) -> str:
    """Return the maze as a plain string with no colors.

    Used when the program is run in a non-interactive environment
    (e.g. piped output, automated testing).

    Args:
        generator: A MazeGenerator instance after generate() was called.
        entry:     (x, y) entrance coordinate.
        exit_:     (x, y) exit coordinate.
        solution:  Solution path string e.g. 'SSSEE'. Empty means no path.

    Returns:
        Multi-line string of the maze.
    """
    # Build the path set from the solution string
    path_set: set[Coord] = set()
    if solution:
        moves = {"N": (0, -1), "E": (1, 0), "S": (0, 1), "W": (-1, 0)}
        x, y = entry
        path_set.add((x, y))
        for step in solution:
            dx, dy = moves[step]
            x += dx
            y += dy
            path_set.add((x, y))

    grid = generator.grid  # type: ignore
    height = generator.height  # type: ignore
    width = generator.width  # type: ignore
    pattern_cells = generator.pattern_cells  # type: ignore
    lines = []

    for row in range(height):
        # Top edge
        top = ""
        for col in range(width):
            top += "+"
            top += "--" if grid[row][col] & NORTH else "  "
        top += "+"
        lines.append(top)

        # Cell row
        cells = ""
        for col in range(width):
            coord = (col, row)
            cells += "|" if grid[row][col] & WEST else " "
            cells += _cell_content(coord, entry, exit_, path_set, bool(solution), pattern_cells)
        cells += "|" if grid[row][width - 1] & EAST else " "
        lines.append(cells)

    # Bottom edge
    bottom = ""
    for col in range(width):
        bottom += "+"
        bottom += "--" if grid[height - 1][col] & SOUTH else "  "
    bottom += "+"
    lines.append(bottom)

    return "\n".join(lines)