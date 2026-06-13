from typing import IO

def display_block(content: str) -> None:
    print("---\n")
    print(content, end="")
    if content and not content.endswith("\n"):
        print()
    print("\n---")

def read_archive(file_name: str) -> str | None:

    print(f"Accessing file '{file_name}'")

    archive_file: IO[str] | None = None
    try:
        archive_file = open(file_name, "r")
        content = archive_file.read()
        cleaned = clean(content.splitlines())
        display_block(cleaned)
        return "\n".join(cleaned)
    except Exception as error:
        print(f"Error opening file '{__name__}': {error}")
        return None
    finally:
        if archive_file is not None:
            archive_file.close()
            print(f"File '{file_name}' closed.\n")

def validate

def dict_converter

def clean(lines: list[str]) -> list[str]:
    result = []
    for line in lines:
        line = line.strip()
        if line and not line.startswith("#"):
            result.append(line)
    return result

"""Configuration parser for the A-Maze-ing project.

Reads a KEY=VALUE config file and validates all mandatory maze settings.

Usage:
    from src.config_parser import parse_config, Config, ConfigError

    config = parse_config("config.txt")
    print(config.width, config.height)
"""

from dataclasses import dataclass
from typing import Optional

# Keys that must be present in every config file
MANDATORY_KEYS = {"WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"}


class ConfigError(Exception):
    """Raised when the config file has invalid or missing values."""
    pass


@dataclass
class Config:
    """Holds all parsed and validated maze configuration values.

    Attributes:
        width:       Number of columns in the maze.
        height:      Number of rows in the maze.
        entry:       (x, y) coordinate of the entrance.
        exit_:       (x, y) coordinate of the exit.
        output_file: Path to write the hex maze output.
        perfect:     If True, maze has exactly one path entry→exit.
        seed:        Optional random seed for reproducibility.
    """

    width: int
    height: int
    entry: tuple[int, int]
    exit_: tuple[int, int]
    output_file: str
    perfect: bool
    seed: Optional[int]


def parse_config(file_path: str) -> Config:
    """Read and validate a maze config file.

    Args:
        file_path: Path to the config file.

    Returns:
        A validated Config object.

    Raises:
        FileNotFoundError: If the file does not exist.
        ConfigError:       If any key is missing or has an invalid value.
    """
    raw = _read_file(file_path)
    pairs = _parse_pairs(raw)
    _check_mandatory_keys(pairs)
    return _build_config(pairs)


# ------------------------------------------------------------------
# Internal helpers
# ------------------------------------------------------------------

def _read_file(file_path: str) -> list[str]:
    """Read the file and return non-empty, non-comment lines.

    Args:
        file_path: Path to the file.

    Returns:
        List of stripped lines with comments and blanks removed.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    with open(file_path, "r") as f:
        lines = f.readlines()

    cleaned = []
    for line in lines:
        line = line.strip()
        if line and not line.startswith("#"):
            cleaned.append(line)
    return cleaned


def _parse_pairs(lines: list[str]) -> dict[str, str]:
    """Split each line on '=' and return a key→value dictionary.

    Args:
        lines: Cleaned lines from the config file.

    Returns:
        Dictionary of uppercase keys to raw string values.

    Raises:
        ConfigError: If a line does not contain exactly one '='.
    """
    pairs: dict[str, str] = {}
    for line in lines:
        if "=" not in line:
            raise ConfigError(f"Invalid line (missing '='): '{line}'")
        key, _, value = line.partition("=")
        key = key.strip().upper()
        value = value.strip()
        if not key:
            raise ConfigError(f"Empty key in line: '{line}'")
        pairs[key] = value
    return pairs


def _check_mandatory_keys(pairs: dict[str, str]) -> None:
    """Raise ConfigError if any mandatory key is missing.

    Args:
        pairs: Parsed key→value dictionary.

    Raises:
        ConfigError: If one or more mandatory keys are absent.
    """
    missing = MANDATORY_KEYS - pairs.keys()
    if missing:
        raise ConfigError(f"Missing required keys: {', '.join(sorted(missing))}")


def _build_config(pairs: dict[str, str]) -> Config:
    """Convert raw string values into typed, validated Config fields.

    Args:
        pairs: Parsed key→value dictionary.

    Returns:
        A fully validated Config object.

    Raises:
        ConfigError: If any value fails type or range validation.
    """
    width = _parse_positive_int(pairs["WIDTH"], "WIDTH")
    height = _parse_positive_int(pairs["HEIGHT"], "HEIGHT")
    entry = _parse_coord(pairs["ENTRY"], "ENTRY", width, height)
    exit_ = _parse_coord(pairs["EXIT"], "EXIT", width, height)
    perfect = _parse_bool(pairs["PERFECT"], "PERFECT")
    output_file = pairs["OUTPUT_FILE"].strip()
    seed = _parse_optional_int(pairs.get("SEED"), "SEED")

    if not output_file:
        raise ConfigError("OUTPUT_FILE cannot be empty.")
    if entry == exit_:
        raise ConfigError("ENTRY and EXIT must be different cells.")

    return Config(
        width=width,
        height=height,
        entry=entry,
        exit_=exit_,
        output_file=output_file,
        perfect=perfect,
        seed=seed,
    )


def _parse_positive_int(value: str, key: str) -> int:
    """Parse a string as a positive integer.

    Args:
        value: Raw string value.
        key:   Key name for error messages.

    Returns:
        Parsed integer.

    Raises:
        ConfigError: If value is not a positive integer.
    """
    try:
        n = int(value)
    except ValueError:
        raise ConfigError(f"{key} must be an integer, got '{value}'.")
    if n < 1:
        raise ConfigError(f"{key} must be a positive integer, got {n}.")
    return n


def _parse_coord(
    value: str,
    key: str,
    width: int,
    height: int,
) -> tuple[int, int]:
    """Parse a 'x,y' string and validate it is inside the maze bounds.

    Args:
        value:  Raw string value e.g. '0,0'.
        key:    Key name for error messages.
        width:  Maze width for bounds check.
        height: Maze height for bounds check.

    Returns:
        Parsed (x, y) coordinate.

    Raises:
        ConfigError: If format is wrong or coordinate is out of bounds.
    """
    parts = value.split(",")
    if len(parts) != 2:
        raise ConfigError(f"{key} must be 'x,y', got '{value}'.")
    try:
        x, y = int(parts[0].strip()), int(parts[1].strip())
    except ValueError:
        raise ConfigError(f"{key} coordinates must be integers, got '{value}'.")
    if not (0 <= x < width and 0 <= y < height):
        raise ConfigError(
            f"{key} ({x},{y}) is outside the maze bounds "
            f"(0..{width - 1}, 0..{height - 1})."
        )
    return (x, y)


def _parse_bool(value: str, key: str) -> bool:
    """Parse 'True' or 'False' (case-insensitive) as a boolean.

    Args:
        value: Raw string value.
        key:   Key name for error messages.

    Returns:
        True or False.

    Raises:
        ConfigError: If value is not 'True' or 'False'.
    """
    if value.strip().lower() == "true":
        return True
    if value.strip().lower() == "false":
        return False
    raise ConfigError(f"{key} must be 'True' or 'False', got '{value}'.")


def _parse_optional_int(value: Optional[str], key: str) -> Optional[int]:
    """Parse an optional integer value.

    Args:
        value: Raw string value, or None if key was absent.
        key:   Key name for error messages.

    Returns:
        Parsed integer, or None if value was absent.

    Raises:
        ConfigError: If value is present but not a valid integer.
    """
    if value is None:
        return None
    try:
        return int(value)
    except ValueError:
        raise ConfigError(f"{key} must be an integer, got '{value}'.")