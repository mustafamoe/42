"""Configuration loading and validation for A-Maze-ing."""

from __future__ import annotations

from pathlib import Path

from mazegen import Coord
from mazegen import MazeGenerator

Config = dict[str, str]


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
    parse_bool(required(config, "PERFECT"), "PERFECT")
    include_pattern = parse_bool(
        config.get("INCLUDE_42", "true"),
        "INCLUDE_42",
    )
    return MazeGenerator(
        width=width,
        height=height,
        entry=entry,
        exit_cell=exit_cell,
        seed=seed,
        include_pattern=include_pattern,
    ).generate()


def output_path(config: Config, config_path: Path) -> Path:
    """Return the configured output path."""
    path = Path(required(config, "OUTPUT_FILE"))
    if not path.is_absolute():
        path = config_path.parent / path
    return path


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
