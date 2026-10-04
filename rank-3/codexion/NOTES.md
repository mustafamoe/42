# Codexion notes

## Authority and scope

- Official input: `resources/en.subject.pdf`, version 1.5, read in full.
- No evaluation sheet or additional campus instructions are supplied locally.
- C, mandatory part only. Norm applies; Libft and global variables are forbidden.
- Rule precedence: subject, supplied campus rules, `docs/42-rules.md`, workflow.
- This project is independent. No implementation was read or copied from another
  workspace project during the 2026-10-04 refactor.

## Mandatory checklist

- [x] Program `codexion`, exactly eight mandatory arguments, exact `fifo` / `edf`.
- [x] One pthread per coder and one separate monitor pthread.
- [x] One mutex-protected dongle per coder; one distinct dongle for N=1.
- [x] Cooldown begins at the synchronized release transition.
- [x] Custom binary heaps; FIFO enqueue order or EDF deadline order with ties.
- [x] A pair can be taken only by the root of both heaps; no priority bypasses.
- [x] Pair reservation and consistent lock order prevent resource deadlock.
- [x] Initial admission/staggering addresses avoidable EDF startup convoys.
- [x] Five exact log messages, serialized printing, one terminal burnout line.
- [x] Expired deadlines cannot be overwritten by starting or finishing a compile.
- [x] Coders remain monitored until the simulation's global stopping condition.
- [x] Completed compile intervals count toward the goal; counts saturate at goal.
- [x] Only subject-authorized external functions and no cross-project dependencies.
- [x] Required English README and Makefile targets/flags.
- [x] Partial allocation, primitive-init, and thread-creation cleanup paths tested.

## Changes on 2026-10-04

Removed the bounded-bypass scheduler and arbitrary heap removal. Acquisition
now checks only the two relevant heap roots, under `state_lock`. The two-pointer
heap storage lives inside each dongle, eliminating N allocations and their
cleanup. Configuration keeps explicit field copies: the local compiler emits an
unlisted `memcpy` call for structure assignment in the required default build.

Removed per-coder condition variables, activation/grant/bypass flags, individual
retirement, and the startup print-signal chain. Workers use one shared condition
for startup, resource waiting, timed activities, and stopping. Two C files were
removed: `scheduler.c` and `heap_remove.c`.

Fixed cooldown timestamping before the state lock, expired compile-start timer
resets, expired completion transitions, and cooldown waits that depended on a
missing wakeup. The print gate remains because it lets the monitor inspect
deadlines independently of a worker's output operation.

## Submission inventory and reading order

The contents of `submission/` become the evaluation repository root:

```text
Makefile
README.md
include/codexion.h
src/main.c
src/parse.c
src/init.c
src/run.c
src/coder.c
src/request.c
src/heap.c
src/dongle.c
src/time.c
src/log.c
src/monitor.c
```

Read in that order. `main` owns setup/run/cleanup; `run` owns thread lifetime;
`coder` owns activity cycles; `request` owns queue admission and pair acquisition;
`heap` owns ordering; `dongle` owns physical availability and release. Logging
and monitoring share the deadline check defined in `monitor.c`.

Private tests, notes, and the subject remain outside `submission/`. Do not submit
objects, the executable, sanitizer binaries, Python caches, or editor settings.

## Inputs and timing

```sh
./codexion 5 800 30 10 10 3 5 edf
```

| Argument | Meaning in the example |
| --- | --- |
| coders | 5 threads and 5 dongles |
| burnout | 800 ms between compile starts, or from simulation start |
| compile | Hold both dongles for at least 30 ms |
| debug | Spend at least 10 ms debugging |
| refactor | Spend at least 10 ms refactoring, then request again |
| goal | Every coder must complete at least 3 compiles |
| cooldown | Released dongles are unavailable for another 5 ms |
| policy | Earliest Deadline First |

Only nonempty decimal digit strings up to `INT_MAX` are accepted. Count,
burnout, and goal must be positive; activity/cooldown durations may be zero.
Invalid arguments or setup failure produce `Error\n` on stderr and exit 1.
A simulated burnout is a normal simulation result and exits 0.

`deadline = last_compile_start + burnout`. Before the first compile, the start
is the common simulation start. Burnout occurs at `now >= deadline`, including
while compiling, debugging, refactoring, waiting, or after reaching an individual
goal. Only global completion or burnout stops the simulation.

A compilation is counted after its full interval and release. Counters saturate
at the goal so repeated cycles cannot increment `completed` twice or overflow
a satisfied coder's count. An `is compiling` line records a start, not a finish.

The former case `6 200 100 1 1 1 20 edf` does not prove successful completion:
three coders start near 0, their neighbors near 120, and the first group burns
out near 200 before the second group finishes near 220. The integration suite
now expects burnout here and uses 260 ms for the completion case.

## Heap and arbitration invariants

A ring dongle has at most two adjacent requesters, each with at most one pending
request. Therefore `t_heap` contains `t_coder *data[2]` and a size. Requests refer
to existing coder objects, without separate request allocation.

- FIFO key: sequence, then coder ID.
- EDF key: `last_compile + burnout`, then sequence, then coder ID.
- Sequence is assigned at enqueue under `state_lock`; it is not OS thread order.
- Deadline is an immutable snapshot while a request is queued.
- `requesting` prevents inserting the same request twice.
- `take_dongles()` requires the same coder at both roots and both dongles ready.
- Pop removes the root. With capacity two, the remaining child becomes the root;
  no arbitrary search or general heap repair is needed.

For four FIFO requests enqueued 1,2,3,4: after coder 1 takes dongles 0 and 1,
coder 3 must wait because coder 2 precedes it on dongle 2. Physical availability
alone never overrides that priority. With initial admission 1,3,2,4, coders 1
and 3 may both take their pairs because each is first on its own two queues.

The same total order in both queues prevents a circular chain of higher-priority
pending requests. Pair acquisition breaks hold-and-wait: a worker never reserves
one distinct dongle while waiting for another. EDF prioritizes the oldest
compile-start deadline; new requests cannot change the key of a waiting request.
These invariants establish resource ordering and progress, while meeting actual
deadlines still depends on feasible timings and OS scheduling.

## Startup and odd-ring spacing

Main creates workers and the monitor, then waits for their readiness before
starting the clock. It queues initial requests by odd IDs, then even IDs. All
initial EDF deadlines are equal; publishing their common start updates all keys
equally, so their heap order is preserved.

The monitor arms before workers leave the startup wait. For odd N > 1, coder
initial sequence q waits until:

```text
start + floor(q * (compile + cooldown) / floor(N / 2))
```

For N=5, compile=100, cooldown=20, initial attempts are spaced at 0,60,120,180,240
ms in order 1,3,5,2,4. This avoids the rigid two-at-a-time wave that can make one
coder wait 360 ms even when a roughly 300 ms repeat interval is possible.
The regression case uses burnout=340 to leave execution margin. Even rings
need no initial stagger. All later requests follow refactoring immediately.

Thread creation happens outside the measured simulation interval. Failed
creation stops and joins only successfully created threads before cleanup.

## Locks and waits

| Shared state | Synchronization during the simulation |
| --- | --- |
| Heaps, sequence, requesting, startup | `state_lock` |
| Dongle held/ready_at | Dongle mutex; state lock surrounds pair transitions |
| last_compile, death_pending, printing | `output_lock` |
| Compile counts and completed count | State then output lock |
| stopped | Writers hold both locks; readers hold at least one |
| Config, IDs, pointers, published start | Immutable after startup publication |

Nested locks are state -> output or state -> dongle locks in increasing index
order. Never acquire state while holding output. The monitor releases output
before taking state during shutdown. A worker may read its own `last_compile`
after logging because only that worker updates it after startup.

| Condition | Mutex | Purpose |
| --- | --- | --- |
| changed | state | Startup, release, activity/cooldown timeouts, shutdown |
| life_changed | output | Compile start, completion, detected burnout, print end |
| print_ready | output | Print gate available or new logs forbidden |

Condition variables carry notifications, not resource ownership. Every wait
rechecks its protected predicate in a loop. A wait releases the associated mutex
atomically and reacquires it before returning, including after spurious wakes.

A requester behind another heap entry or a held dongle waits for a state change.
When first in both queues with free but cooling dongles, it timed-waits until
the later `ready_at`. The timestamp comes from that same availability check;
if it passes before sleeping, the wait helper returns immediately. Release
broadcasts `changed`, so previously indefinite waiters learn about new cooldowns.

`held` is the logical reservation; a dongle mutex is not held during compilation.
Release takes state and both dongle mutexes before setting both cooldown ends
and clearing both held flags. Lock contention cannot consume cooldown early.

`wait_changed()` is called with state locked. It uses a condition timeout
until 10 ms before the target, then releases the lock for 500 us sleeps near
the deadline. Each caller rechecks its predicate after reacquiring state. This
limits polling to the end of timed waits while reducing accumulated timer
coalescing: on this host a plain 20 ms timeout was measured up to about 10 ms
late, enough to break a tight but otherwise feasible EDF cycle.

`gettimeofday` supplies epoch milliseconds. Absolute condition timeouts use
that same real-time clock domain. Wall-clock adjustments and arbitrarily slow
OS scheduling/stdout remain environmental limits; this is not hard real time.

## Logging, burnout, and completion

`simulation_active()` requires `output_lock`. It checks stopped/death-pending
state and every coder's deadline. The first detected expired ID is saved in
`death_pending`; the monitor and blocked printers are notified.

Before an ordinary log, `begin_log()` waits for the print gate, samples time,
and checks all deadlines. For a compile it updates `last_compile` under the
same lock. Completion uses that same check before changing counts, so neither
a late worker nor a delayed monitor can erase an already-expired deadline.

A printer owns the protected gate while `printf` runs without `output_lock`.
The monitor can inspect deadlines during output. Only the monitor prints death:
it waits for an active batch, claims the gate, prints once, and stops/wakes all
workers. A compile batch contains three lines, not just one message. The gate
prevents any ordinary message after the burnout line.

On success, the last required completed compile sets stopped and wakes both
monitor and workers. A worker that reached its own goal earlier still cycles
and can burn out before global completion. For one coder, a single take is
logged; it cannot compile using the same dongle twice.

## Validation

Run from the workspace root:

```sh
DEVELOPER_DIR=/Library/Developer/CommandLineTools sh rank-3/codexion/tests/test.sh
uvx norminette rank-3/codexion/submission/include rank-3/codexion/submission/src
uvx --python python3.10 flake8 rank-3/codexion/tests/test.py
uvx --python python3.10 mypy --strict rank-3/codexion/tests/test.py
```

The local macOS toolchain needs the Command Line Tools override above. The
Makefile remains portable and uses `cc -Wall -Wextra -Werror -pthread`.

`tests/regression.c` privately includes implementation files to exercise internal
transitions without adding production test hooks. Its fake clock and injected
lock delay check the release boundary deterministically. It covers strict
FIFO/EDF, disjoint grants, EDF ties, heap pop, cooldown, expired starts and
completions, global completion, and every allocation/init/thread-create failure
position. Test-only globals and injected wrappers are not submitted.

`tests/test.py` uses Python 3.10 and bounded subprocess timeouts. It checks invalid
inputs, both policies, zero durations, one coder, compile/debug/refactor timing,
neighbor resource spacing, cooldown, odd/even EDF cases, the global stop rule,
log format, burnout latency, and absence of output after burnout. It distinguishes
starts from completed work and requires at least the requested compile count.
The shell runner builds, checks no relink is needed, runs both suites, and cleans.

Finite tests are evidence for the checked workloads, not a proof of optimal
scheduling for every numerical input. Keep the subject's OS/hardware tolerance
in mind when measuring its 10 ms burnout reporting requirement.

### Results, 2026-10-04

- Required warning-clean build, incremental no-relink check, and Norm: pass.
- C regression suite and 23 integration scenarios, including 52 invalid-input
  variations: pass. Python 3.10, flake8, and strict mypy: pass.
- The same regression and integration suites pass with AddressSanitizer plus
  UndefinedBehaviorSanitizer, and separately with ThreadSanitizer.
- `leaks --atExit` reports zero leaked bytes for a normal simulation and the
  regression process, including all injected setup failures.
- 85 repeated runs pass: tight 5/7/9-coder EDF cases, the 5-coder debug/refactor
  case, the 6-coder completion case, and 200-coder burnout timing.
- Deliberately restoring each of four faults makes a regression assertion fail:
  priority bypass, early cooldown timestamp, expired start, expired completion.
- A standalone copy builds and runs without sibling projects. Submission has
  no symlinks, cross-project paths, or generated artifacts.
- Submitted C/header size decreased from 1,283 to 1,023 lines (about 20%), with
  11 C files instead of 13. Counts include Norm headers and blank lines.
