# Fly-in Notes

## Status

Mandatory code validated against the supplied subject, evaluation sheet, and
all nine mandatory maps. The in-person algorithm explanation and live coding
exercise still require the learner's demonstration during the defense.

## Official Inputs

- `resources/en.subject.pdf`: Fly-in subject, version 1.6, 24 pages.
- `resources/evaluation-sheet.pdf`: supplied 2026-10-14, seven pages read in
  full with rendered checks of the parser, benchmark, and live coding sections.
  Title: `Intra Projects Fly-in Edit`; printed date: 2026-08-16. No scale version
  is stated. The original attachment is preserved unchanged; SHA-256:
  `95f65a8547d7b1e6396d162b282152142be9e051586f0d56d56d9e5b72a86ba4`.
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
- [x] Requires positive regular-zone and connection capacities.
- [x] Ignores start/end `max_drones` values as required; metadata syntax is
  still validated.
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

| Map | Turns | Reference target |
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

## Readability Review (2026-10-14)

The module responsibilities, domain models, CLI, and rendering are already
clear. The main source of friction was repeatedly passing four pieces of A*
bookkeeping between the planner helpers.

- `_RouteSearch` groups one drone's search queue, insertion counter, best
  priority penalties, and predecessor records. It is recreated for each drone;
  zone and connection reservations remain on `RoutePlanner` across drones.
- The queue entry type documents its ordering. Search locals use `turn`, and
  comments explain the time bound, reverse movement costs, restricted arrival
  checks, and same-turn capacity reuse.
- The parser uses `drone_count is None` to recognize the first declaration
  instead of a redundant flag. `_fail()` returns `NoReturn`, so the type checker
  understands that parsing stops there without an assertion or unreachable
  re-raise.

To follow execution, start at `FlyInApplication.run()`, then read
`MapParser.parse()`, `RoutePlanner.plan()`, and `Simulation.run()`. For routing,
`_find_route()` expands `(zone, turn)` states; `_consider_wait()` and
`_consider_move()` check capacity, `_offer()` records useful continuations,
and `_reserve()` protects a completed route for later drones.

Validation used Python 3.10. All six existing tests, flake8, and the required
mypy checks pass. The test suite audits capacity safety and target turn counts
on all nine mandatory maps. Their CLI output matches the original source byte
for byte, retaining the benchmark results above. A temporary comparison also
matched parsed networks, complete routes and rendered output or planning errors
on 100 generated maps, plus the same parsing errors on seven malformed maps.
The routing algorithm and submission inventory are unchanged.

## Evaluation Sheet Audit (2026-10-14)

The attached scale adds explicit checks for colors, error categories, higher
drone counts, larger graphs, and a live coding exercise. Private tests now
cover these code checks rather than relying on the original six tests alone.

Two parser gaps were reproduced and fixed:

- Numeric text beyond Python's integer conversion limit now produces a
  line-specific parsing error instead of an uncaught `ValueError`. Very large
  capacities within the supported integer size are accepted, including
  `10**100`. This does not impose a new drone or capacity limit.
- Start/end capacity values are ignored, including zero and negative values,
  following the subject's specific unlimited-endpoint exception. Regular hubs
  and connections still reject non-positive or non-integer capacities.

The README now has the scale's Algorithm Explanation section. It describes
the planning trade-off: each drone gets its earliest route while earlier
reservations stay fixed; this is not a proof of globally optimal scheduling
on every unseen graph.

| Scale section | Evidence and result |
| --- | --- |
| Submission | Standalone export has exactly the eight intended root files. |
| README | Required sections, visualization, and executable example present. |
| OOP and graph | Domain, parser, planner, simulation, and view classes; custom adjacency lists; standard-library imports only. |
| Type safety and style | `mypy .`, required `make lint` flags, and flake8 pass. |
| Valid map format | Drone declaration, hubs, links, defaults, metadata order, and comments pass. |
| Parser errors | All five scale categories pass, plus malformed metadata, unknown endpoints, and numeric conversion limits. |
| Occupancy and movement | Independent route audit checks zone/link capacities, unlimited endpoints, same-turn release, and exact restricted arrival. |
| Priority and blocked zones | Priority wins an equal-time route; blocked paths are excluded. |
| Visualization | Red/blue destination colors and `NO_COLOR` tested in a real pseudo-terminal; redirected output is plain. |
| Basic output and completion | Correct movement tokens, omitted stationary/delivered drones, and immediate final termination. |
| Pathfinding and conflicts | All nine supplied maps and a 50-drone, 120-zone graph produce safe routes. |
| Edge cases | All five listed groups pass: one drone, bottlenecks, disconnected graphs, invalid connections, and zero/high capacities. |
| Object lifetime | Twenty repeated simulations retain no network, planner, route, or simulation objects after cleanup. |
| Benchmarks | All nine maps beat their individual reference targets; averages are 4 turns easy, 8 medium, and 18.33 hard. |
| Explanation and live coding | Human defense tasks; preparation below, not marked as completed by automation. |

The medium scale describes an expected 10–30-turn average; this implementation
averages 8 turns and beats each supplied medium target. The schedule is faster
than that expected band, and no artificial waiting has been added.
The challenger map is optional and remains outside this mandatory audit.

The expanded suite has **17 tests**, with additional subcases for malformed
maps and capacities. A fresh standalone copy passed `make install`, `make
lint`, plain `mypy .`, all 17 tests, the README example, all nine map CLI runs,
`make run`, `make debug`, and `make clean`. The copy used its own Python 3.10
virtual environment and no sibling project files. Source hashes and command
results are saved in `tests/evaluation-audit.json`.

## Defense Preparation: `--capacity-info`

Page 6 asks the learner to add and demonstrate this flag within ten minutes
during the defense. It is a live modification exercise, so it is not
preimplemented in the baseline submission or counted as an automated pass.

The minimal change belongs in three existing places:

1. In `FlyInApplication.run()`, recognize and remove `--capacity-info` from
   the command-line arguments before validating the single map path. Pass
   the resulting boolean into `Simulation`; give it a default of `False`.
2. In `Simulation.run()`, gather capacity counts while walking the complete
   route actions. Initialize typed zone/link usage dictionaries with
   `defaultdict(int)` from `collections`. Count zone occupancy before the
   `action.is_wait` skip, because a waiting drone still occupies its zone.
   Count connection use only for traversal actions:

   ```python
   if action.destination not in (self._network.start, self._network.end):
       zone_usage[(action.destination, action.end_time)] += 1
   if action.connection is not None:
       link_usage[(action.connection.key, action.start_time + 1)] += 1
   ```

3. Give `TerminalView.show()` optional capacity lines indexed by turn. Print
   them after each existing movement line only when the flag is enabled.
   For each regular zone use `Zone X: Y/Z drones`, and for each connection
   use `Connection A-B: Y/Z capacity used`. Report unused resources as zero;
   start/end zones have unlimited capacity and must not use their stored
   `max_drones` value as a limit.

Use the README's one-drone restricted example for the demonstration. Expected
capacity information for its finite resources is:

| Turn | tunnel zone | start-tunnel connection | tunnel-goal connection |
| --- | --- | --- | --- |
| 1 | 0/1 | 1/1 | 0/1 |
| 2 | 1/1 | 0/1 | 0/1 |
| 3 | 0/1 | 0/1 | 1/1 |

Then demonstrate two drones through a capacity-one middle zone: the second
drone enters on the turn the first leaves, and the displayed zone count stays
at one. Run without the flag too and verify the normal movement output stays
identical. Be ready to explain why restricted transit counts a link on the
first turn and its destination on the next, and why waiting must be counted.
