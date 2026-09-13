#!/usr/bin/env python3
"""Command-line entry point for the Fly-in drone simulation."""

import sys
from pathlib import Path
from typing import List

from parser import MapParser, ParseError
from planner import PlanningError, RoutePlanner
from simulation import Simulation, TerminalView


class FlyInApplication:
    """Coordinate parsing, planning, and rendering for one map."""

    def run(self, arguments: List[str]) -> int:
        """Run the application and return a process exit status."""
        if len(arguments) != 2:
            print(f"Usage: {arguments[0]} <map_file>", file=sys.stderr)
            return 1
        try:
            network = MapParser().parse(Path(arguments[1]))
            routes = RoutePlanner(network).plan()
            Simulation(network, routes, TerminalView()).run()
        except (ParseError, PlanningError) as error:
            print(f"Error: {error}", file=sys.stderr)
            return 1
        return 0


def main() -> int:
    """Run Fly-in with the current command-line arguments."""
    return FlyInApplication().run(sys.argv)


if __name__ == "__main__":
    raise SystemExit(main())
