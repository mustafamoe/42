"""Turn-by-turn output and terminal visualization for Fly-in."""

import os
import sys
from dataclasses import dataclass
from typing import Dict, List, TextIO, Tuple

from models import DroneRoute, NetworkMap


@dataclass(frozen=True)
class Movement:
    """One printable drone movement event."""

    drone_id: int
    target: str
    color: str


class TerminalView:
    """Render movement tokens with map-requested terminal colors."""

    _COLORS = {
        "black": 30,
        "red": 31,
        "green": 32,
        "yellow": 33,
        "blue": 34,
        "purple": 35,
        "magenta": 35,
        "cyan": 36,
        "white": 37,
        "gray": 90,
        "grey": 90,
        "orange": 208,
        "brown": 130,
        "lime": 118,
        "gold": 220,
        "maroon": 88,
        "darkred": 88,
        "violet": 129,
        "crimson": 197,
        "rainbow": 201,
    }

    def __init__(self, stream: TextIO = sys.stdout) -> None:
        """Enable color only on an interactive terminal."""
        self._stream = stream
        self._use_color = stream.isatty() and "NO_COLOR" not in os.environ

    def show(self, turns: Dict[int, List[Movement]], last_turn: int) -> None:
        """Print every simulation turn in chronological order."""
        for turn in range(1, last_turn + 1):
            movements = sorted(
                turns.get(turn, []), key=lambda movement: movement.drone_id
            )
            tokens = [self._token(movement) for movement in movements]
            print(" ".join(tokens), file=self._stream)

    def _token(self, movement: Movement) -> str:
        """Format one movement, adding color when useful and safe."""
        token = f"D{movement.drone_id}-{movement.target}"
        if not self._use_color or movement.color == "none":
            return token
        code = self._COLORS.get(movement.color.lower(), 37)
        if code < 100:
            return f"\033[{code}m{token}\033[0m"
        return f"\033[38;5;{code}m{token}\033[0m"


class Simulation:
    """Convert planned routes into mandatory movement output."""

    def __init__(
        self,
        network: NetworkMap,
        routes: Tuple[DroneRoute, ...],
        view: TerminalView,
    ) -> None:
        """Store the immutable plan and its output view."""
        self._network = network
        self._routes = routes
        self._view = view

    def run(self) -> None:
        """Render all route actions as one line per turn."""
        turns: Dict[int, List[Movement]] = {}
        last_turn = 0
        for route in self._routes:
            last_turn = max(last_turn, route.arrival_time)
            for action in route.actions:
                if action.is_wait:
                    continue
                assert action.connection is not None
                destination = self._network.zones[action.destination]
                if action.end_time - action.start_time == 2:
                    self._add(
                        turns,
                        action.start_time + 1,
                        Movement(
                            route.drone_id,
                            action.connection.label,
                            destination.color,
                        ),
                    )
                self._add(
                    turns,
                    action.end_time,
                    Movement(
                        route.drone_id,
                        action.destination,
                        destination.color,
                    ),
                )
        self._view.show(turns, last_turn)

    def _add(
        self,
        turns: Dict[int, List[Movement]],
        turn: int,
        movement: Movement,
    ) -> None:
        """Append one movement to its output turn."""
        turns.setdefault(turn, []).append(movement)
