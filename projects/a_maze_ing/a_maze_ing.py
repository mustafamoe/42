#!/usr/bin/env python3
"""Command line entrypoint for the A-Maze-ing project."""

from __future__ import annotations

import sys
from pathlib import Path

from mazegen import EAST
from mazegen import NORTH
from mazegen import SOUTH
from mazegen import WEST
from mazegen import Coord
from mazegen import MazeGenerator

Config = dict[str, str]

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


def load_config(path: Path) -> Config:
    """Read KEY=VALUE entries from the configuration file."""
    config: Config = {}
    for line_number, raw_line in enumerate(path.read_text().splitlines(), 1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            raise ValueError(f"line {line_number}: expected KEY=VALUE")
        key, value = line.split("=", 1)
        key = key.strip().upper()
        value = value.strip()
        if not key:
            raise ValueError(f"line {line_number}: empty key")
        if key in config:
            raise ValueError(f"line {line_number}: duplicate key {key}")
        config[key] = value
    return config


def build_generator(
    config: Config,
    seed_override: int | None,
) -> MazeGenerator:
    """Create and generate a MazeGenerator from a parsed config."""
    width = parse_int(required(config, "WIDTH"), "WIDTH")
    height = parse_int(required(config, "HEIGHT"), "HEIGHT")
    entry = parse_coord(required(config, "ENTRY"), "ENTRY")
    exit_cell = parse_coord(required(config, "EXIT"), "EXIT")
    seed = seed_override
    if seed is None:
        seed = parse_seed(config.get("SEED", "42"))
    perfect = parse_bool(required(config, "PERFECT"), "PERFECT")
    include_pattern = parse_bool(
        config.get("INCLUDE_42", config.get("ADD_42_PATTERN", "true")),
        "INCLUDE_42",
    )
    extra = parse_float(
        config.get("EXTRA_OPENINGS", "0.12"),
        "EXTRA_OPENINGS",
    )
    return MazeGenerator(
        width=width,
        height=height,
        entry=entry,
        exit_cell=exit_cell,
        seed=seed,
        perfect=perfect,
        extra_openings=extra,
        include_pattern=include_pattern,
    ).generate()


def required(config: Config, key: str) -> str:
    """Return a required config value."""
    if key not in config:
        raise ValueError(f"missing required config key {key}")
    return config[key]


def parse_int(value: str, key: str) -> int:
    """Parse an integer config value."""
    try:
        return int(value)
    except ValueError as error:
        raise ValueError(f"{key} must be an integer") from error


def parse_float(value: str, key: str) -> float:
    """Parse a floating point config value."""
    try:
        return float(value)
    except ValueError as error:
        raise ValueError(f"{key} must be a number") from error


def parse_seed(value: str) -> int | None:
    """Parse a reproducibility seed, allowing RANDOM for ad hoc mazes."""
    normalized = value.strip().lower()
    if normalized == "random":
        return None
    return parse_int(value, "SEED")


def parse_bool(value: str, key: str) -> bool:
    """Parse a boolean config value."""
    normalized = value.strip().lower()
    if normalized in ("1", "true", "yes", "on"):
        return True
    if normalized in ("0", "false", "no", "off"):
        return False
    raise ValueError(f"{key} must be true or false")


def parse_coord(value: str, key: str) -> Coord:
    """Parse an x,y coordinate."""
    pieces = [piece.strip() for piece in value.split(",")]
    if len(pieces) != 2:
        raise ValueError(f"{key} must use x,y format")
    return (parse_int(pieces[0], key), parse_int(pieces[1], key))


def output_path(config: Config, config_path: Path) -> Path:
    """Return the configured output path."""
    path = Path(required(config, "OUTPUT_FILE"))
    if not path.is_absolute():
        path = config_path.parent / path
    return path


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


def interactive_loop(
    config: Config,
    config_path: Path,
    generator: MazeGenerator,
    show_path: bool,
    color: str,
) -> None:
    """Run the optional terminal control loop."""
    out_path = output_path(config, config_path)
    current = parse_seed(config.get("SEED", "42"))
    print_menu(show_path, color)
    while True:
        try:
            command = input("menu> ").strip()
        except EOFError:
            print()
            return
        normalized = command.lower()
        if normalized in ("0", "quit", "q", "exit"):
            return
        if normalized in ("help", "h", "?"):
            print_menu(show_path, color)
            continue
        if normalized in ("1", "new", "regen", "regenerate"):
            current = None if current is None else current + 1
            generator = build_generator(config, current)
            write_output(out_path, generator)
            print_result(generator, out_path, show_path, color)
        elif normalized in ("2", "path", "toggle"):
            show_path = not show_path
            print_result(generator, out_path, show_path, color)
        elif normalized in ("3", "color", "colour", "wall", "walls"):
            color = choose_wall_color(color)
            print_result(generator, out_path, show_path, color)
        elif normalized in ("4", "save", "write"):
            write_output(out_path, generator)
            print(f"Saved: {out_path}")
        elif normalized.startswith(("color ", "colour ")):
            color = handle_color_command(command, color)
            print_result(generator, out_path, show_path, color)
        else:
            print("Unknown option. Type help for the menu.")
            continue
        print_menu(show_path, color)


def print_menu(show_path: bool, color: str) -> None:
    """Print the visible interaction menu required by the subject."""
    path_state = "shown" if show_path else "hidden"
    print()
    print("Menu")
    print("1. Re-generate a new maze")
    print(f"2. Show/Hide shortest path (currently {path_state})")
    print(f"3. Change maze wall colour (currently {color})")
    print("4. Save output file again")
    print("0. Quit")


def handle_color_command(command: str, current: str) -> str:
    """Parse and apply a color command."""
    pieces = command.split()
    if len(pieces) == 1:
        names = ", ".join(COLOR_NAMES)
        print(f"Colors: {names}")
        return current
    if len(pieces) != 2:
        print("Usage: color NAME")
        return current
    try:
        return normalize_color(pieces[1])
    except ValueError as error:
        print(error)
        return current


def choose_wall_color(current: str) -> str:
    """Prompt for a wall color from the visible menu."""
    print()
    for index, name in enumerate(COLOR_NAMES, 1):
        marker = " *" if name == current else ""
        print(f"{index}. {name}{marker}")
    try:
        choice = input("Wall colour name or number: ").strip().lower()
    except EOFError:
        print()
        return current
    if not choice:
        return current
    if choice.isdigit():
        index = int(choice)
        if 1 <= index <= len(COLOR_NAMES):
            return COLOR_NAMES[index - 1]
        print("Unknown colour number.")
        return current
    try:
        return normalize_color(choice)
    except ValueError as error:
        print(error)
        return current


def main(argv: list[str]) -> int:
    """Run the CLI program."""
    if len(argv) != 2:
        print("Usage: ./a_maze_ing.py config.txt", file=sys.stderr)
        return 1

    config_path = Path(argv[1])
    try:
        config = load_config(config_path)
        generator = build_generator(config, None)
        out_path = output_path(config, config_path)
        show_path = parse_bool(config.get("SHOW_PATH", "false"), "SHOW_PATH")
        color = normalize_color(config.get("WALL_COLOR", "plain"))
        display = config.get("DISPLAY", "terminal").strip().lower()
        if display != "terminal":
            raise ValueError("DISPLAY must be terminal")
        interactive = parse_bool(
            config.get("INTERACTIVE", "true"),
            "INTERACTIVE",
        )
        write_output(out_path, generator)
        print_result(generator, out_path, show_path, color)
        if interactive:
            if sys.stdin.isatty():
                interactive_loop(
                    config,
                    config_path,
                    generator,
                    show_path,
                    color,
                )
            else:
                print_menu(show_path, color)
        return 0
    except (OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nInterrupted.", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
