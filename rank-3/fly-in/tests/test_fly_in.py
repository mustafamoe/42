"""Private compliance tests for the Fly-in submission."""

import io
import sys
import tempfile
import unittest
from collections import defaultdict
from pathlib import Path
from typing import DefaultDict, Tuple

SUBMISSION = Path(__file__).resolve().parents[1] / "submission"
MAPS = Path(__file__).resolve().parents[1] / "resources" / "maps"
sys.path.insert(0, str(SUBMISSION))

from models import DroneRoute, NetworkMap, ZoneType  # noqa: E402
from parser import MapParser, ParseError  # noqa: E402
from planner import PlanningError, RoutePlanner  # noqa: E402
from simulation import Simulation, TerminalView  # noqa: E402


class FlyInTestCase(unittest.TestCase):
    """Test parsing, planning, capacity safety, and rendering."""

    def parse_text(self, text: str) -> NetworkMap:
        """Parse a temporary map and return its network model."""
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "map.txt"
            path.write_text(text, encoding="utf-8")
            return MapParser().parse(path)

    def assert_valid_routes(
        self, network: NetworkMap, routes: Tuple[DroneRoute, ...]
    ) -> None:
        """Independently audit resource usage in a planned schedule."""
        zone_usage: DefaultDict[Tuple[str, int], int] = defaultdict(int)
        edge_usage: DefaultDict[Tuple[Tuple[str, str], int], int]
        edge_usage = defaultdict(int)
        self.assertEqual(len(routes), network.drone_count)
        for route in routes:
            current = network.start
            current_time = 0
            for action in route.actions:
                self.assertEqual(action.origin, current)
                self.assertEqual(action.start_time, current_time)
                if action.is_wait:
                    self.assertEqual(action.destination, current)
                    self.assertEqual(action.end_time, current_time + 1)
                else:
                    self.assertIsNotNone(action.connection)
                    connection = action.connection
                    assert connection is not None
                    self.assertEqual(connection.other(current), action.destination)
                    destination = network.zones[action.destination]
                    self.assertIsNot(destination.kind, ZoneType.BLOCKED)
                    self.assertEqual(
                        action.end_time - action.start_time,
                        destination.travel_time,
                    )
                    slot = (connection.key, action.start_time + 1)
                    edge_usage[slot] += 1
                    self.assertLessEqual(edge_usage[slot], connection.capacity)
                current = action.destination
                current_time = action.end_time
                if current not in (network.start, network.end):
                    zone_usage[(current, current_time)] += 1
                    self.assertLessEqual(
                        zone_usage[(current, current_time)],
                        network.zones[current].max_drones,
                    )
            self.assertEqual(current, network.end)
            self.assertEqual(current_time, route.arrival_time)

    def test_all_mandatory_maps_are_safe_and_within_targets(self) -> None:
        """Solve and audit every supplied easy, medium, and hard map."""
        targets = {
            "easy/01_linear_path.txt": 6,
            "easy/02_simple_fork.txt": 8,
            "easy/03_basic_capacity.txt": 6,
            "medium/01_dead_end_trap.txt": 12,
            "medium/02_circular_loop.txt": 15,
            "medium/03_priority_puzzle.txt": 12,
            "hard/01_maze_nightmare.txt": 30,
            "hard/02_capacity_hell.txt": 35,
            "hard/03_ultimate_challenge.txt": 45,
        }
        for relative_path, target in targets.items():
            with self.subTest(map=relative_path):
                network = MapParser().parse(MAPS / relative_path)
                routes = RoutePlanner(network).plan()
                self.assert_valid_routes(network, routes)
                self.assertLessEqual(
                    max(route.arrival_time for route in routes), target
                )

    def test_parser_accepts_comments_defaults_and_metadata_order(self) -> None:
        """Accept valid optional metadata and required defaults."""
        network = self.parse_text(
            """# comment before the first declaration
nb_drones: 2
start_hub: start 0 0 [max_drones=99 color=green]
hub: fast 1 -2 [max_drones=3 color=cyan zone=priority]
end_hub: goal 2 0
connection: start-fast [max_link_capacity=2]
connection: fast-goal
"""
        )
        self.assertEqual(network.zones["start"].max_drones, 1)
        self.assertEqual(network.zones["fast"].max_drones, 3)
        self.assertIs(network.zones["fast"].kind, ZoneType.PRIORITY)
        self.assertEqual(network.zones["goal"].color, "none")

    def test_parser_reports_line_and_cause(self) -> None:
        """Reject malformed maps with a useful line-specific error."""
        invalid_maps = (
            (
                "hub: wrong 0 0\n",
                "line 1: first declaration must be nb_drones",
            ),
            (
                """nb_drones: 1
start_hub: start 0 0
end_hub: goal 1 0
connection: start-goal
connection: goal-start
""",
                "line 5: duplicate connection",
            ),
            (
                """nb_drones: 1
start_hub: start 0 0
end_hub: goal 1 0
connection: start-missing
""",
                "line 4: unknown zone 'missing'",
            ),
            (
                """nb_drones: 1
start_hub: start 0 0
end_hub: goal 1 0
connection: start-goal
hub: late 2 0
""",
                "line 5: zones must be declared before connections",
            ),
            (
                """nb_drones: 0
start_hub: start 0 0
end_hub: goal 1 0
""",
                "line 1: nb_drones must be a positive integer",
            ),
        )
        for text, message in invalid_maps:
            with self.subTest(message=message):
                with self.assertRaisesRegex(ParseError, message):
                    self.parse_text(text)

    def test_restricted_zone_uses_connection_then_destination(self) -> None:
        """Print the declared connection label during restricted transit."""
        network = self.parse_text(
            """nb_drones: 1
start_hub: start 0 0
hub: tunnel 1 0 [zone=restricted color=red]
end_hub: goal 2 0
connection: start-tunnel
connection: tunnel-goal
"""
        )
        routes = RoutePlanner(network).plan()
        output = io.StringIO()
        Simulation(network, routes, TerminalView(output)).run()
        self.assertEqual(
            output.getvalue(),
            "D1-start-tunnel\nD1-tunnel\nD1-goal\n",
        )

    def test_capacity_is_reused_after_a_same_turn_departure(self) -> None:
        """Allow a following drone to enter as the occupant leaves."""
        network = self.parse_text(
            """nb_drones: 2
start_hub: start 0 0
hub: middle 1 0
end_hub: goal 2 0
connection: start-middle
connection: middle-goal
"""
        )
        routes = RoutePlanner(network).plan()
        self.assert_valid_routes(network, routes)
        self.assertEqual(max(route.arrival_time for route in routes), 3)

    def test_blocked_route_is_rejected_cleanly(self) -> None:
        """Raise a planning error when blocked zones cut the only route."""
        network = self.parse_text(
            """nb_drones: 1
start_hub: start 0 0
hub: wall 1 0 [zone=blocked]
end_hub: goal 2 0
connection: start-wall
connection: wall-goal
"""
        )
        with self.assertRaisesRegex(PlanningError, "no accessible route"):
            RoutePlanner(network).plan()


if __name__ == "__main__":
    unittest.main()
