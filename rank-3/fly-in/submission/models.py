"""Domain models for Fly-in maps and planned drone routes."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple


class ZoneType(Enum):
    """Supported zone types from the Fly-in map format."""

    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"


@dataclass(frozen=True)
class Zone:
    """A named location in the drone network."""

    name: str
    x: int
    y: int
    kind: ZoneType = ZoneType.NORMAL
    color: str = "none"
    max_drones: int = 1

    @property
    def travel_time(self) -> int:
        """Return the number of turns required to enter this zone."""
        if self.kind is ZoneType.RESTRICTED:
            return 2
        return 1

    @property
    def preference_penalty(self) -> int:
        """Return a tie-break penalty that favors priority zones."""
        if self.kind is ZoneType.PRIORITY:
            return 0
        return 1


@dataclass(frozen=True)
class Connection:
    """A bidirectional, capacity-limited connection between two zones."""

    first: str
    second: str
    capacity: int = 1

    @property
    def key(self) -> Tuple[str, str]:
        """Return the direction-independent identity of the connection."""
        if self.first <= self.second:
            return (self.first, self.second)
        return (self.second, self.first)

    @property
    def label(self) -> str:
        """Return the connection text in its declared input order."""
        return f"{self.first}-{self.second}"

    def other(self, zone_name: str) -> str:
        """Return the endpoint opposite to the supplied zone name."""
        if zone_name == self.first:
            return self.second
        if zone_name == self.second:
            return self.first
        raise ValueError(
            f"zone '{zone_name}' is not on connection '{self.label}'"
        )


@dataclass
class NetworkMap:
    """A parsed Fly-in map with an adjacency-list representation."""

    drone_count: int
    zones: Dict[str, Zone]
    connections: Tuple[Connection, ...]
    start: str
    end: str
    adjacency: Dict[str, List[Connection]] = field(init=False)

    def __post_init__(self) -> None:
        """Build adjacency lists after validating parser-owned fields."""
        self.adjacency = {name: [] for name in self.zones}
        for connection in self.connections:
            self.adjacency[connection.first].append(connection)
            self.adjacency[connection.second].append(connection)

    def has_capacity(self, zone_name: str, occupied: int) -> bool:
        """Return whether another drone may occupy the zone."""
        if zone_name == self.start or zone_name == self.end:
            return True
        return occupied < self.zones[zone_name].max_drones


@dataclass(frozen=True)
class RouteAction:
    """A wait or connection traversal in one planned drone route."""

    start_time: int
    end_time: int
    origin: str
    destination: str
    connection: Optional[Connection]

    @property
    def is_wait(self) -> bool:
        """Return whether this action keeps the drone in place."""
        return self.connection is None


@dataclass(frozen=True)
class DroneRoute:
    """The complete conflict-free plan for one drone."""

    drone_id: int
    actions: Tuple[RouteAction, ...]
    arrival_time: int
