"""Capacity-aware route planning for Fly-in."""

import heapq
from collections import defaultdict
from dataclasses import dataclass, field
from itertools import count
from typing import DefaultDict, Dict, List, Tuple

from models import (
    Connection,
    DroneRoute,
    NetworkMap,
    RouteAction,
    ZoneType,
)

State = Tuple[str, int]
EdgeSlot = Tuple[Tuple[str, str], int]
ZoneSlot = Tuple[str, int]
Previous = Tuple[State, RouteAction]
# Heap order: estimated arrival, current turn, priority penalty, order, zone.
SearchEntry = Tuple[int, int, int, int, str]


@dataclass
class _RouteSearch:
    """Keep A* bookkeeping local to one drone's route search."""

    queue: List[SearchEntry] = field(default_factory=list)
    tie_breaker: count = field(default_factory=count)
    best_preference: Dict[State, int] = field(default_factory=dict)
    previous: Dict[State, Previous] = field(default_factory=dict)


class PlanningError(Exception):
    """Report a map for which no valid drone plan can be built."""


class RoutePlanner:
    """Plan earliest conflict-free routes using time-slot reservations."""

    def __init__(self, network: NetworkMap) -> None:
        """Initialize static distances and empty resource reservations."""
        self._network = network
        self._zone_usage: DefaultDict[ZoneSlot, int] = defaultdict(int)
        self._edge_usage: DefaultDict[EdgeSlot, int] = defaultdict(int)
        self._heuristic = self._distances_to_end()
        self._latest_arrival = 0

    def plan(self) -> Tuple[DroneRoute, ...]:
        """Plan every drone in identifier order and reserve its route."""
        if self._network.start not in self._heuristic:
            raise PlanningError("no accessible route from start to end")
        routes: List[DroneRoute] = []
        for drone_id in range(1, self._network.drone_count + 1):
            route = self._find_route(drone_id)
            self._reserve(route)
            routes.append(route)
            self._latest_arrival = max(
                self._latest_arrival, route.arrival_time
            )
        return tuple(routes)

    def _find_route(self, drone_id: int) -> DroneRoute:
        """Find the earliest route available to one drone."""
        start_state = (self._network.start, 0)
        shortest_time = self._heuristic[self._network.start]
        # Once earlier drones arrive, waiting at start leaves a clear route.
        time_limit = self._latest_arrival + shortest_time
        search = _RouteSearch(best_preference={start_state: 0})
        heapq.heappush(
            search.queue,
            (shortest_time, 0, 0, next(search.tie_breaker),
             self._network.start),
        )

        while search.queue:
            _, turn, preference, _, zone_name = heapq.heappop(search.queue)
            state = (zone_name, turn)
            if search.best_preference.get(state) != preference:
                continue
            if zone_name == self._network.end:
                actions = self._reconstruct(state, search.previous)
                return DroneRoute(drone_id, actions, turn)
            if turn >= time_limit:
                continue

            self._consider_wait(state, preference, time_limit, search)
            for connection in self._ordered_connections(zone_name):
                self._consider_move(
                    state, preference, connection, time_limit, search,
                )

        raise PlanningError(f"unable to plan drone {drone_id}")

    def _consider_wait(
        self,
        state: State,
        preference: int,
        time_limit: int,
        search: _RouteSearch,
    ) -> None:
        """Add a one-turn wait when the zone retains capacity."""
        zone_name, turn = state
        next_turn = turn + 1
        if next_turn > time_limit:
            return
        occupied = self._zone_usage[(zone_name, next_turn)]
        if not self._network.has_capacity(zone_name, occupied):
            return
        next_state = (zone_name, next_turn)
        action = RouteAction(turn, next_turn, zone_name, zone_name, None)
        self._offer(next_state, preference, action, state, search)

    def _consider_move(
        self,
        state: State,
        preference: int,
        connection: Connection,
        time_limit: int,
        search: _RouteSearch,
    ) -> None:
        """Add a traversal when its edge and destination have capacity."""
        zone_name, turn = state
        destination = connection.other(zone_name)
        zone = self._network.zones[destination]
        if zone.kind is ZoneType.BLOCKED or destination not in self._heuristic:
            return
        arrival_time = turn + zone.travel_time
        if arrival_time > time_limit:
            return
        edge_slot = (connection.key, turn + 1)
        if self._edge_usage[edge_slot] >= connection.capacity:
            return
        # Check arrival capacity before accepting a restricted traversal.
        occupied = self._zone_usage[(destination, arrival_time)]
        if not self._network.has_capacity(destination, occupied):
            return

        next_state = (destination, arrival_time)
        next_preference = preference + zone.preference_penalty
        action = RouteAction(
            turn,
            arrival_time,
            zone_name,
            destination,
            connection,
        )
        self._offer(
            next_state, next_preference, action, state, search,
        )

    def _offer(
        self,
        state: State,
        preference: int,
        action: RouteAction,
        origin: State,
        search: _RouteSearch,
    ) -> None:
        """Record a better path to a time-expanded state."""
        known = search.best_preference.get(state)
        if known is not None and known <= preference:
            return
        zone_name, turn = state
        search.best_preference[state] = preference
        search.previous[state] = (origin, action)
        estimate = turn + self._heuristic[zone_name]
        heapq.heappush(
            search.queue,
            (estimate, turn, preference, next(search.tie_breaker), zone_name),
        )

    def _ordered_connections(self, zone_name: str) -> List[Connection]:
        """Return useful connections with priority destinations first."""
        def key(connection: Connection) -> Tuple[int, int, str]:
            """Build a stable shortest-path-friendly ordering key."""
            destination = connection.other(zone_name)
            zone = self._network.zones[destination]
            distance = self._heuristic.get(destination, 10**12)
            return (zone.preference_penalty, distance, destination)

        return sorted(self._network.adjacency[zone_name], key=key)

    def _reconstruct(
        self, state: State, previous: Dict[State, Previous]
    ) -> Tuple[RouteAction, ...]:
        """Reconstruct route actions from predecessor records."""
        actions: List[RouteAction] = []
        while state in previous:
            state, action = previous[state]
            actions.append(action)
        actions.reverse()
        return tuple(actions)

    def _reserve(self, route: DroneRoute) -> None:
        """Reserve all finite-capacity time slots used by a route."""
        # End-of-turn occupancy allows another drone to enter after departure.
        for action in route.actions:
            if action.connection is not None:
                edge_slot = (action.connection.key, action.start_time + 1)
                self._edge_usage[edge_slot] += 1
            if (
                action.destination != self._network.start
                and action.destination != self._network.end
            ):
                zone_slot = (action.destination, action.end_time)
                self._zone_usage[zone_slot] += 1

    def _distances_to_end(self) -> Dict[str, int]:
        """Compute an admissible weighted distance from every useful zone."""
        end_zone = self._network.zones[self._network.end]
        if end_zone.kind is ZoneType.BLOCKED:
            return {}
        distances: Dict[str, int] = {self._network.end: 0}
        queue: List[Tuple[int, str]] = [(0, self._network.end)]
        while queue:
            distance, zone_name = heapq.heappop(queue)
            if distances.get(zone_name) != distance:
                continue
            # Reverse search charges entry into the zone we came back from.
            entry_cost = self._network.zones[zone_name].travel_time
            for connection in self._network.adjacency[zone_name]:
                neighbor = connection.other(zone_name)
                neighbor_zone = self._network.zones[neighbor]
                if (
                    neighbor_zone.kind is ZoneType.BLOCKED
                    and neighbor != self._network.start
                ):
                    continue
                candidate = distance + entry_cost
                if candidate < distances.get(neighbor, 10**12):
                    distances[neighbor] = candidate
                    heapq.heappush(queue, (candidate, neighbor))
        return distances
