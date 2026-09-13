*This project has been created as part of the 42 curriculum by mal-hall.*

# Fly-in

## Description

Fly-in routes a fleet of drones from one start hub to one end hub through a
capacity-limited network. It parses the subject map format, avoids blocked
zones, coordinates simultaneous movement, uses alternate paths when useful,
and handles the two-turn cost of entering restricted zones.

The implementation is fully object-oriented and uses only the Python 3.10
standard library. The terminal displays movements in each destination zone's
configured color when standard output is interactive. Redirected or piped
output stays plain so that it remains easy to validate.

## Instructions

Python 3.10 or later is required. Install the development checks with:

```sh
make install
```

Run a map directly or through the Makefile:

```sh
python3.10 fly_in.py path/to/map.txt
make run MAP=path/to/map.txt
```

Other required commands are:

```sh
make debug MAP=path/to/map.txt
make lint
make clean
```

The program writes parsing and planning errors to standard error and exits
with a non-zero status. Valid simulations print one line per turn. A drone
that waits is omitted from that turn, and a delivered drone is not printed
again.

## Algorithm and Strategy

1. `MapParser` validates each declaration and creates `Zone`, `Connection`,
   and `NetworkMap` objects. The network stores connections in adjacency
   lists; no graph library is used.
2. `RoutePlanner` runs a reverse weighted shortest-path search to obtain an
   admissible estimate from every accessible zone to the end. Entering a
   normal or priority zone costs one turn; entering a restricted zone costs
   two turns.
3. Drones are planned in identifier order. For each drone, an A* search over
   `(zone, turn)` states finds its earliest conflict-free arrival. A state may
   wait or traverse a connection. Routes already selected for earlier drones
   reserve exact zone and connection time slots, so later routes cannot exceed
   either capacity. Start and end capacities are unlimited.
4. Equal-time choices use a secondary penalty that prefers priority zones.
   Blocked zones are never expanded. A restricted traversal reserves its
   connection on the first turn and its destination on the following turn,
   which guarantees that the drone cannot remain in transit or arrive at a
   full zone.
5. `Simulation` converts the completed plans into chronological movement
   lines. Because occupancy is reserved at the end of each turn, a drone may
   enter a zone during the same turn that another drone leaves it.

For `D` drones, `V` zones, `E` connections, and a latest searched turn `T`,
the worst-case planning time is
`O(D * T * (V + E) * log(T * V))`. Search memory is `O(T * V)`, plus the
reserved schedule. The practical search horizon is bounded by the latest
existing arrival plus the unconstrained shortest travel time.

## Restricted Connection Output

The map format gives connections no separate name. During the first turn of a
restricted traversal, Fly-in therefore prints the exact endpoint pair in the
order declared by the input, for example `D1-start-tunnel`. On the next turn
it prints the restricted destination, for example `D1-tunnel`.

## Visual Representation

Movement tokens use ANSI terminal colors that correspond to each destination
zone's `color` metadata. This makes parallel routes, merges, and restricted
transits easier to follow during a live evaluation without adding extra lines
or changing the required token format. Setting the standard `NO_COLOR`
environment variable, redirecting output, or piping it disables color.

## Example

Input:

```text
nb_drones: 1

start_hub: start 0 0 [color=green]
hub: tunnel 1 0 [zone=restricted color=red]
end_hub: goal 2 0 [color=blue]

connection: start-tunnel
connection: tunnel-goal
```

Output:

```text
D1-start-tunnel
D1-tunnel
D1-goal
```

## Resources

- Fly-in subject, version 1.6, supplied through 42 Intra.
- Official Fly-in challenge maps supplied with the subject.
- Python 3.10 documentation for `dataclasses`, `enum`, `heapq`, `pathlib`,
  `re`, and `typing`.
- *Introduction to Algorithms*, fourth edition, for shortest-path concepts.

Codex AI was used to extract the supplied requirements, help design and write
the implementation, create private tests, and prepare this documentation. All
generated work was checked against the subject, `flake8`, `mypy`, and the
official mandatory maps. The author remains responsible for understanding and
being able to explain or modify every submitted component.
