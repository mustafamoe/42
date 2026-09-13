# Fly-in Notes

## Status

Mandatory implementation complete and validated against the supplied subject
and all nine mandatory maps. No evaluation sheet was supplied, so any
evaluation-sheet-only requirement remains unaudited.

## Official Inputs

- `resources/en.subject.pdf`: Fly-in subject, version 1.6, 24 pages.
- `resources/maps/`: 10 supplied maps plus their README.
- The challenger map is optional bonus material and did not add features or
  files to the submission.

## Design Summary

- `models.py`: typed domain objects and the adjacency-list network.
- `parser.py`: line-aware parser with subject defaults and validation.
- `planner.py`: time-expanded A* routing with resource reservations.
- `simulation.py`: mandatory movement events and TTY-only color rendering.
- `fly_in.py`: small command-line application coordinator.

Each drone is assigned its earliest currently available route. Existing routes
reserve `(zone, turn)` and `(connection, turn)` slots. This makes waiting and
same-turn capacity release explicit, prevents conflicts by construction, and
avoids a separate deadlock-resolution system.

## Mandatory Compliance Checklist

### Project and Tooling

- [x] Uses Python 3.10 or later.
- [x] Implementation is object-oriented and type-safe.
- [x] All submitted Python code has type hints and passes required `mypy`.
- [x] All submitted code passes `flake8`.
- [x] Modules, classes, functions, and methods have PEP 257 docstrings.
- [x] Expected failures are handled cleanly; file reading uses a context
  manager.
- [x] Uses no graph library or third-party runtime dependency.
- [x] Submission contains a Python `.gitignore`.
- [x] Makefile includes `install`, `run`, `debug`, `clean`, and `lint`.
- [x] `lint` runs the exact subject-required checks.

### Parser

- [x] Requires a positive `nb_drones` as the first data declaration.
- [x] Requires exactly one start and one end.
- [x] Parses unique dash-free names and integer coordinates.
- [x] Parses metadata in any order and applies documented defaults.
- [x] Accepts only normal, blocked, restricted, and priority zone types.
- [x] Requires positive zone and connection capacities.
- [x] Parses but ignores start/end `max_drones` as required.
- [x] Requires zones before connections and known connection endpoints.
- [x] Rejects duplicate bidirectional and self-connections.
- [x] Removes comments beginning with `#`.
- [x] Reports the line number and cause for malformed declarations.

### Routing, Output, and Visualization

- [x] Supports any positive drone count without a hard-coded limit.
- [x] Uses weighted alternate routes, waiting, and priority tie-breaking.
- [x] Avoids blocked zones, conflicts, and deadlocks.
- [x] Enforces zone and bidirectional connection capacities per turn.
- [x] Treats start and end as unlimited and reuses same-turn departures.
- [x] Restricted entry takes exactly two turns and guarantees arrival capacity.
- [x] Prints only `D<ID>-<target>` movements, separated by spaces.
- [x] Omits stationary and delivered drones.
- [x] Uses map-requested terminal colors without polluting redirected output.
- [x] Ends only when all drones reach the end.

### Documentation

- [x] Required English README is at the submission root.
- [x] First line contains the italicized 42 attribution and `mal-hall` login.
- [x] README covers use, strategy, complexity, visualization, example,
  resources, and AI assistance.

## Restricted Connection Convention

The subject asks for a connection name during restricted transit, but its map
grammar defines only an endpoint pair. The implementation prints that pair in
the exact order declared in the map (`first-second`). This is the smallest
deterministic interpretation and preserves the official input text.

## Mandatory Benchmark Results

| Map | Turns | Required maximum |
| --- | ---: | ---: |
| easy/01_linear_path | 4 | 6 |
| easy/02_simple_fork | 4 | 8 |
| easy/03_basic_capacity | 4 | 6 |
| medium/01_dead_end_trap | 8 | 12 |
| medium/02_circular_loop | 10 | 15 |
| medium/03_priority_puzzle | 6 | 12 |
| hard/01_maze_nightmare | 13 | 30 |
| hard/02_capacity_hell | 16 | 35 |
| hard/03_ultimate_challenge | 26 | 45 |

## Validation Commands

From `submission/`:

```text
make lint
python3.10 -m unittest discover -s ../tests -v
python3.10 -m compileall -q .
```

The private test suite independently reconstructs zone and connection usage
for all mandatory schedules. It also covers malformed input, reversed duplicate
connections, undefined zones, declarations in the wrong order, invalid drone
counts, metadata defaults, blocked routes, restricted output, and same-turn
capacity reuse.

## Exact Submission Inventory

- `.gitignore`
- `Makefile`
- `README.md`
- `fly_in.py`
- `models.py`
- `parser.py`
- `planner.py`
- `simulation.py`

Do not copy `resources/`, `tests/`, `NOTES.md`, caches, environments, logs, or
generated output to the evaluation repository.
