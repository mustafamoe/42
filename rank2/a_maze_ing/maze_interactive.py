"""Interactive terminal menu for A-Maze-ing."""

from __future__ import annotations

from pathlib import Path

from mazegen import MazeGenerator
from maze_config import Config
from maze_config import build_generator
from maze_config import output_path
from maze_config import parse_seed
from maze_output import write_output
from maze_render import COLOR_NAMES
from maze_render import normalize_color
from maze_render import print_result


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
