"""Tests for the A-Maze-ing CLI helper modules."""

from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from maze_config import build_generator
from maze_config import load_config
from maze_config import output_path
from maze_output import write_output
from maze_render import normalize_color
from maze_render import render_maze


CONFIG_TEXT = """\
WIDTH=4
HEIGHT=4
ENTRY=0,0
EXIT=3,3
SEED=7
PERFECT=true
INCLUDE_42=false
OUTPUT_FILE=maze.txt
"""


class CliModuleTests(unittest.TestCase):
    """Verify the small CLI modules still work together."""

    def test_config_builds_generator_and_relative_output_path(self) -> None:
        with TemporaryDirectory() as tmp_name:
            config_path = Path(tmp_name) / "config.txt"
            config_path.write_text(CONFIG_TEXT)

            config = load_config(config_path)
            generator = build_generator(config, None)
            resolved_output = output_path(config, config_path)

        self.assertEqual(resolved_output, config_path.parent / "maze.txt")
        self.assertEqual(generator.entry, (0, 0))
        self.assertEqual(generator.exit, (3, 3))
        self.assertEqual(len(generator.to_hex_rows()), 4)
        self.assertTrue(generator.solution_path())

    def test_render_and_output_use_generated_maze(self) -> None:
        with TemporaryDirectory() as tmp_name:
            config_path = Path(tmp_name) / "config.txt"
            output_file = Path(tmp_name) / "maze.txt"
            config_path.write_text(CONFIG_TEXT)
            generator = build_generator(load_config(config_path), None)

            write_output(output_file, generator)
            rendered = render_maze(
                generator,
                show_path=True,
                wall_color="plain",
            )

            saved_lines = output_file.read_text().splitlines()

        self.assertIn(" S ", rendered)
        self.assertIn(" E ", rendered)
        self.assertEqual(saved_lines[5], "0,0")
        self.assertEqual(saved_lines[6], "3,3")
        self.assertEqual(saved_lines[7], generator.solution_path())

    def test_normalize_color_rejects_unknown_colors(self) -> None:
        self.assertEqual(normalize_color(" CYAN "), "cyan")
        with self.assertRaises(ValueError):
            normalize_color("orange")


if __name__ == "__main__":
    unittest.main()
