#!/usr/bin/env python3
"""Command line entrypoint for the A-Maze-ing project."""

from __future__ import annotations

import sys
from pathlib import Path

from maze_config import build_generator
from maze_config import load_config
from maze_config import output_path
from maze_config import parse_bool
from maze_interactive import interactive_loop
from maze_interactive import print_menu
from maze_output import write_output
from maze_render import normalize_color
from maze_render import print_result


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
