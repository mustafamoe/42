"""Parser for the Fly-in map language."""

import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from models import Connection, NetworkMap, Zone, ZoneType


class ParseError(Exception):
    """Report an invalid map with a precise line and cause."""


class MapParser:
    """Parse and validate a Fly-in map file."""

    _DRONES = re.compile(r"^nb_drones:\s*(\S+)\s*$")
    _ZONE = re.compile(
        r"^(start_hub|hub|end_hub):\s+([^\s\-\[\]]+)\s+"
        r"([+-]?\d+)\s+([+-]?\d+)(?:\s+\[([^\]]*)\])?\s*$"
    )
    _CONNECTION = re.compile(
        r"^connection:\s+([^\s\-\[\]]+)-([^\s\-\[\]]+)"
        r"(?:\s+\[([^\]]*)\])?\s*$"
    )

    def parse(self, path: Path) -> NetworkMap:
        """Read, parse, and validate one map file."""
        try:
            with path.open("r", encoding="utf-8") as source:
                lines = source.readlines()
        except (OSError, UnicodeError) as error:
            raise ParseError(f"cannot read '{path}': {error}") from error

        drone_count: Optional[int] = None
        zones: Dict[str, Zone] = {}
        connections: List[Connection] = []
        connection_keys: set[Tuple[str, str]] = set()
        start: Optional[str] = None
        end: Optional[str] = None
        first_data_seen = False
        connections_started = False

        for line_number, raw_line in enumerate(lines, start=1):
            text = raw_line.split("#", 1)[0].strip()
            if not text:
                continue
            if not first_data_seen:
                drone_count = self._parse_drone_count(text, line_number)
                first_data_seen = True
                continue

            zone_match = self._ZONE.fullmatch(text)
            if zone_match is not None:
                if connections_started:
                    self._fail(
                        line_number,
                        "zones must be declared before connections",
                    )
                role, zone = self._parse_zone(zone_match, line_number)
                if zone.name in zones:
                    self._fail(line_number, f"duplicate zone '{zone.name}'")
                if role == "start_hub":
                    if start is not None:
                        self._fail(line_number, "more than one start_hub")
                    start = zone.name
                elif role == "end_hub":
                    if end is not None:
                        self._fail(line_number, "more than one end_hub")
                    end = zone.name
                zones[zone.name] = zone
                continue

            connection_match = self._CONNECTION.fullmatch(text)
            if connection_match is not None:
                connections_started = True
                connection = self._parse_connection(
                    connection_match, zones, line_number
                )
                if connection.key in connection_keys:
                    self._fail(
                        line_number,
                        f"duplicate connection '{connection.label}'",
                    )
                connection_keys.add(connection.key)
                connections.append(connection)
                continue

            self._fail(line_number, "unrecognized or malformed declaration")

        if drone_count is None:
            raise ParseError("parse error: missing nb_drones declaration")
        if start is None:
            raise ParseError("parse error: expected exactly one start_hub")
        if end is None:
            raise ParseError("parse error: expected exactly one end_hub")
        return NetworkMap(
            drone_count,
            zones,
            tuple(connections),
            start,
            end,
        )

    def _parse_drone_count(self, text: str, line_number: int) -> int:
        """Parse the required first data declaration."""
        match = self._DRONES.fullmatch(text)
        if match is None:
            self._fail(line_number, "first declaration must be nb_drones")
        assert match is not None
        value = self._positive_integer(
            match.group(1), line_number, "nb_drones"
        )
        return value

    def _parse_zone(
        self, match: re.Match[str], line_number: int
    ) -> Tuple[str, Zone]:
        """Create a zone from one validated declaration match."""
        role, name, x_text, y_text, metadata_text = match.groups()
        metadata = self._metadata(metadata_text, line_number)
        allowed = {"zone", "color", "max_drones"}
        self._reject_unknown(metadata, allowed, line_number)

        kind_text = metadata.get("zone", ZoneType.NORMAL.value)
        try:
            kind = ZoneType(kind_text)
        except ValueError as error:
            self._fail(line_number, f"invalid zone type '{kind_text}'")
            raise error

        color = metadata.get("color", "none")
        if not color or any(character.isspace() for character in color):
            self._fail(line_number, "color must be a single word")

        max_drones = 1
        if "max_drones" in metadata:
            parsed_capacity = self._positive_integer(
                metadata["max_drones"], line_number, "max_drones"
            )
            if role == "hub":
                max_drones = parsed_capacity

        return role, Zone(
            name=name,
            x=int(x_text),
            y=int(y_text),
            kind=kind,
            color=color,
            max_drones=max_drones,
        )

    def _parse_connection(
        self,
        match: re.Match[str],
        zones: Dict[str, Zone],
        line_number: int,
    ) -> Connection:
        """Create a connection whose endpoints already exist."""
        first, second, metadata_text = match.groups()
        if first == second:
            self._fail(
                line_number,
                "a connection cannot join a zone to itself",
            )
        for endpoint in (first, second):
            if endpoint not in zones:
                self._fail(line_number, f"unknown zone '{endpoint}'")

        metadata = self._metadata(metadata_text, line_number)
        self._reject_unknown(metadata, {"max_link_capacity"}, line_number)
        capacity = 1
        if "max_link_capacity" in metadata:
            capacity = self._positive_integer(
                metadata["max_link_capacity"],
                line_number,
                "max_link_capacity",
            )
        return Connection(first, second, capacity)

    def _metadata(
        self, text: Optional[str], line_number: int
    ) -> Dict[str, str]:
        """Parse optional bracket metadata into unique key-value pairs."""
        values: Dict[str, str] = {}
        if text is None or not text.strip():
            return values
        for item in text.split():
            if item.count("=") != 1:
                self._fail(line_number, f"invalid metadata item '{item}'")
            key, value = item.split("=", 1)
            if not key or not value:
                self._fail(line_number, f"invalid metadata item '{item}'")
            if key in values:
                self._fail(line_number, f"duplicate metadata key '{key}'")
            values[key] = value
        return values

    def _reject_unknown(
        self,
        metadata: Dict[str, str],
        allowed: set[str],
        line_number: int,
    ) -> None:
        """Reject metadata keys not defined by the subject."""
        for key in metadata:
            if key not in allowed:
                self._fail(line_number, f"unknown metadata key '{key}'")

    def _positive_integer(
        self, text: str, line_number: int, field_name: str
    ) -> int:
        """Parse one strictly positive decimal integer."""
        if not text.isdecimal() or int(text) <= 0:
            self._fail(line_number, f"{field_name} must be a positive integer")
        return int(text)

    def _fail(self, line_number: int, cause: str) -> None:
        """Raise a consistently formatted line-specific parse error."""
        raise ParseError(f"parse error on line {line_number}: {cause}")
