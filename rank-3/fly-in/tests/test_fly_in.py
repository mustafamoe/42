"""Private compliance tests for the Fly-in submission."""

import gc
import io
import subprocess
import sys
import tempfile
import unittest
import weakref
from collections import defaultdict
from pathlib import Path
from typing import DefaultDict, Tuple
from unittest.mock import patch

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
                    self.assertEqual(
                        connection.other(current), action.destination
                    )
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

    def test_all_parser_error_categories_from_evaluation(self) -> None:
        """Reject malformed syntax, missing hubs, types, and capacities."""
        valid = (
            "nb_drones: 1\nstart_hub: start 0 0\n"
            "hub: middle 1 0\nend_hub: goal 2 0\n"
            "connection: start-middle\nconnection: middle-goal\n"
        )
        cases = [
            ("", "missing nb_drones"),
            (valid.replace("nb_drones: 1\n", ""), "first declaration"),
            (valid.replace("start_hub: start 0 0\n", ""), "unknown zone"),
            (valid.replace("start_hub:", "hub:"), "exactly one start_hub"),
            (valid.replace("end_hub:", "hub:"), "exactly one end_hub"),
            (valid.replace("hub: middle 1 0", "hub: middle 1 0 [zone=bad]"),
             "invalid zone type"),
            (valid.replace("hub: middle 1 0", "hub: middle x 0"),
             "malformed declaration"),
            (valid.replace("hub: middle 1 0", "hub: middle 1 0 [color=]"),
             "invalid metadata"),
            (valid.replace("hub: middle 1 0", "hub: middle 1 0 [color=red"),
             "malformed declaration"),
            (valid.replace(
                "hub: middle 1 0",
                "hub: middle 1 0 [zone=normal zone=priority]",
            ),
             "duplicate metadata key"),
            (valid.replace("hub: middle 1 0", "hub: middle 1 0 [unknown=1]"),
             "unknown metadata key"),
            (valid.replace(
                "hub: middle 1 0", "hub: middle 1 0\nhub: middle 2 0"
            ),
             "duplicate zone"),
            (valid + "connection: goal-middle\n", "duplicate connection"),
            (valid.replace("start-middle", "start-absent"), "unknown zone"),
            (valid.replace("start-middle", "start-start"),
             "join a zone to itself"),
        ]
        for capacity in ("0", "-2", "1.5", "abc"):
            cases.append((valid.replace(
                "hub: middle 1 0", f"hub: middle 1 0 [max_drones={capacity}]"
            ), "max_drones must be a positive integer"))
            cases.append((valid.replace(
                "connection: start-middle",
                f"connection: start-middle [max_link_capacity={capacity}]"
            ), "max_link_capacity must be a positive integer"))
        for text, message in cases:
            with self.subTest(message=message, text=text):
                with self.assertRaisesRegex(ParseError, message):
                    self.parse_text(text)

    def test_start_and_end_capacity_metadata_is_ignored(self) -> None:
        """Ignore hub capacity values at the two unlimited endpoints."""
        network = self.parse_text(
            "nb_drones: 4\n"
            "start_hub: start 0 0 [max_drones=0]\n"
            "end_hub: goal 1 0 [max_drones=-2]\n"
            "connection: start-goal [max_link_capacity=4]\n"
        )
        routes = RoutePlanner(network).plan()
        self.assert_valid_routes(network, routes)
        self.assertTrue(all(route.arrival_time == 1 for route in routes))

    def test_priority_zone_wins_an_equal_time_route(self) -> None:
        """Choose the priority branch even when it is declared later."""
        network = self.parse_text(
            "nb_drones: 1\nstart_hub: start 0 0\n"
            "hub: ordinary 1 0\nhub: preferred 1 1 [zone=priority]\n"
            "end_hub: goal 2 0\nconnection: start-ordinary\n"
            "connection: ordinary-goal\nconnection: start-preferred\n"
            "connection: preferred-goal\n"
        )
        routes = RoutePlanner(network).plan()
        self.assert_valid_routes(network, routes)
        self.assertEqual(routes[0].arrival_time, 2)
        self.assertEqual(routes[0].actions[0].destination, "preferred")

    def test_zone_capacity_limits_a_wider_connection(self) -> None:
        """Allow two drones, rather than three, in a two-slot middle zone."""
        network = self.parse_text(
            "nb_drones: 4\nstart_hub: start 0 0\n"
            "hub: middle 1 0 [max_drones=2]\nend_hub: goal 2 0\n"
            "connection: start-middle [max_link_capacity=3]\n"
            "connection: middle-goal [max_link_capacity=3]\n"
        )
        routes = RoutePlanner(network).plan()
        self.assert_valid_routes(network, routes)
        self.assertEqual(
            [route.arrival_time for route in routes], [2, 2, 3, 3]
        )

    def test_large_connection_capacity_allows_parallel_arrivals(self) -> None:
        """Support high capacities and more than ten drones without limits."""
        network = self.parse_text(
            "nb_drones: 20\nstart_hub: start 0 0\nend_hub: goal 1 0\n"
            f"connection: start-goal [max_link_capacity={10 ** 100}]\n"
        )
        routes = RoutePlanner(network).plan()
        self.assert_valid_routes(network, routes)
        self.assertEqual(len(routes), 20)
        self.assertTrue(all(route.arrival_time == 1 for route in routes))

    def test_large_graph_routes_many_drones_safely(self) -> None:
        """Audit fifty drones across a 120-zone graph with weighted zones."""
        width, height = 12, 10
        lines = ["nb_drones: 50"]
        for y in range(height):
            for x in range(width):
                role = "hub"
                kind = "normal"
                if (x, y) == (0, 0):
                    role = "start_hub"
                elif (x, y) == (width - 1, height - 1):
                    role = "end_hub"
                elif (x + y) % 7 == 0:
                    kind = "restricted"
                elif (x + y) % 3 == 0:
                    kind = "priority"
                lines.append(
                    f"{role}: z{x}_{y} {x} {y} "
                    f"[zone={kind} max_drones=2]"
                )
        for y in range(height):
            for x in range(width):
                for next_x, next_y in ((x + 1, y), (x, y + 1)):
                    if next_x < width and next_y < height:
                        lines.append(
                            f"connection: z{x}_{y}-z{next_x}_{next_y} "
                            "[max_link_capacity=2]"
                        )
        network = self.parse_text("\n".join(lines))
        routes = RoutePlanner(network).plan()
        self.assertEqual(len(network.zones), 120)
        self.assertEqual(len(routes), 50)
        self.assert_valid_routes(network, routes)

    def test_restricted_arrivals_cannot_wait_on_connections(self) -> None:
        """Guarantee next-turn arrival at a contested restricted zone."""
        network = self.parse_text(
            "nb_drones: 3\nstart_hub: start 0 0\n"
            "hub: tunnel 1 0 [zone=restricted]\nend_hub: goal 2 0\n"
            "connection: start-tunnel [max_link_capacity=3]\n"
            "connection: tunnel-goal [max_link_capacity=3]\n"
        )
        routes = RoutePlanner(network).plan()
        self.assert_valid_routes(network, routes)
        output = io.StringIO()
        Simulation(network, routes, TerminalView(output)).run()
        self.assertEqual(output.getvalue().splitlines(), [
            "D1-start-tunnel", "D1-tunnel D2-start-tunnel",
            "D1-goal D2-tunnel D3-start-tunnel", "D2-goal D3-tunnel",
            "D3-goal",
        ])

    def test_stationary_and_delivered_drones_are_omitted(self) -> None:
        """Print movement only, and stop immediately after final delivery."""
        network = self.parse_text(
            "nb_drones: 3\nstart_hub: start 0 0\n"
            "hub: middle 1 0\nend_hub: goal 2 0\n"
            "connection: start-middle\nconnection: middle-goal\n"
        )
        output = io.StringIO()
        Simulation(
            network, RoutePlanner(network).plan(), TerminalView(output)
        ).run()
        self.assertEqual(output.getvalue().splitlines(), [
            "D1-middle", "D1-goal D2-middle", "D2-goal D3-middle", "D3-goal",
        ])

    def test_colors_follow_destination_metadata_on_a_terminal(self) -> None:
        """Color movement tokens on terminals and honor NO_COLOR."""
        network = self.parse_text(
            "nb_drones: 1\nstart_hub: start 0 0\n"
            "hub: tunnel 1 0 [zone=restricted color=red]\n"
            "end_hub: goal 2 0 [color=blue]\n"
            "connection: start-tunnel\nconnection: tunnel-goal\n"
        )
        routes = RoutePlanner(network).plan()
        for no_color in (False, True):
            with self.subTest(no_color=no_color):
                output = io.StringIO()
                environment = {"NO_COLOR": "1"} if no_color else {}
                with (
                    patch.dict("os.environ", environment, clear=True),
                    patch.object(output, "isatty", return_value=True),
                ):
                    Simulation(network, routes, TerminalView(output)).run()
                if no_color:
                    self.assertNotIn("\033[", output.getvalue())
                else:
                    self.assertEqual(output.getvalue().splitlines(), [
                        "\033[31mD1-start-tunnel\033[0m",
                        "\033[31mD1-tunnel\033[0m",
                        "\033[34mD1-goal\033[0m",
                    ])

    def test_cli_errors_are_clear_and_do_not_crash(self) -> None:
        """Report usage, missing files, disconnections, and numeric limits."""
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "map.txt"
            cases = [
                ([], None),
                ([str(path)], None),
                ([str(path)], "nb_drones: 1\nstart_hub: start 0 0\n"
                 "end_hub: goal 1 0\n"),
                ([str(path)],
                 "nb_drones: 1\nstart_hub: start 0 0 [zone=bad]\n"),
            ]
            for arguments, content in cases:
                if content is not None:
                    path.write_text(content, encoding="utf-8")
                result = subprocess.run(
                    [sys.executable, str(SUBMISSION / "fly_in.py"),
                     *arguments],
                    text=True, capture_output=True, timeout=5,
                )
                self.assertEqual(result.returncode, 1)
                self.assertEqual(result.stdout, "")
                self.assertNotIn("Traceback", result.stderr)
                self.assertTrue(result.stderr.startswith(("Usage:", "Error:")))

            for field in ("coordinate", "capacity", "drone_count"):
                with self.subTest(field=field):
                    digits = "9" * 5000
                    content = (
                        "nb_drones: 1\nstart_hub: start 0 0\n"
                        "end_hub: goal 1 0\nconnection: start-goal\n"
                    )
                    if field == "coordinate":
                        content = content.replace(
                            "start 0 0", f"start {digits} 0"
                        )
                    elif field == "capacity":
                        content = content.replace(
                            "start-goal",
                            f"start-goal [max_link_capacity={digits}]",
                        )
                    else:
                        content = content.replace(
                            "nb_drones: 1", f"nb_drones: {digits}"
                        )
                    path.write_text(content, encoding="utf-8")
                    result = subprocess.run(
                        [sys.executable, str(SUBMISSION / "fly_in.py"),
                         str(path)],
                        text=True, capture_output=True, timeout=5,
                    )
                    self.assertEqual(result.returncode, 1)
                    self.assertNotIn("Traceback", result.stderr)
                    self.assertIn("parse error on line", result.stderr)

    def test_repeated_simulations_release_their_objects(self) -> None:
        """Keep no network, planner, route, or simulation alive after a run."""
        references = []
        for _ in range(20):
            network = self.parse_text(
                "nb_drones: 2\nstart_hub: start 0 0\nend_hub: goal 1 0\n"
                "connection: start-goal\n"
            )
            planner = RoutePlanner(network)
            routes = planner.plan()
            simulation = Simulation(
                network, routes, TerminalView(io.StringIO())
            )
            simulation.run()
            references.extend(
                weakref.ref(item)
                for item in (network, planner, simulation, *routes)
            )
            del simulation, routes, planner, network
        gc.collect()
        self.assertTrue(all(reference() is None for reference in references))


if __name__ == "__main__":
    unittest.main()
