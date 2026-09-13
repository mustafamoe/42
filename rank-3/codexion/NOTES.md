# Codexion notes

## Authority

- Subject: `resources/en.subject.pdf`, version 1.5.
- Intra project page checked on 2026-08-30.
- No evaluation sheet or additional project asset was exposed on Intra.
- Rule precedence: subject, supplied Intra instructions, `docs/42-rules.md`,
  then workflow defaults.

## Mandatory checklist

- [x] C program named `codexion`.
- [x] Exact eight arguments and `fifo` / `edf` scheduler validation.
- [x] One thread per coder and one separate monitor thread.
- [x] One mutex-protected dongle per coder.
- [x] Cooldown enforced after every dongle release.
- [x] Every dongle uses a custom binary heap for fair FIFO or EDF access.
- [x] EDF equal-deadline ties are deterministic.
- [x] Output is serialized and uses the five exact required messages.
- [x] Burnout is monitored independently and stops the simulation.
- [x] The simulation also stops after every coder reaches the compile goal.
- [x] No global variables, Libft, bonus, or non-subject dependency.
- [x] Required English README and Makefile targets.

## Minimal design

Each coder inserts one immutable request into both adjacent dongle heaps. Pairs
are granted atomically. Arbitration considers only requests whose complete pair
is currently available, while the best blocked request becomes a reservation
barrier after at most one overlapping bypass. EDF permits that bypass only when
the lower request's compile and cooldown finish by the protected deadline.
Disjoint eligible pairs can still run concurrently. This avoids head-of-line
convoys while bounding interference and preventing starvation.

### Arbitration interpretation to defend

The subject states FIFO/EDF ordering for each contested dongle but does not say
how to combine two queues when their heads cannot acquire a complete pair. This
implementation orders complete, pair-ready requests and permits a bounded
bypass of a blocked request. A strict "head of both heaps" interpretation would
obey each queue literally but serialize the ring through head-of-line convoys,
causing avoidable EDF starvation for otherwise feasible parameters. The README
states the chosen pair-ready interpretation explicitly. If a campus evaluation
sheet later defines strict per-dongle head ownership, the scheduler must be
revisited rather than silently claiming both interpretations are equivalent.

FIFO orders by a monotonic request sequence; EDF orders by burnout deadline,
then request sequence and coder ID. The monitor is armed before coder work
begins. A worker-readiness barrier keeps thread creation outside the simulation
clock. Per-coder conditions avoid a start-up wake storm, and initial granted
coders start through a short signal chain. Compile start time is recorded at
the visible compile event rather than at scheduler grant time.

Lifecycle timestamps and completion flags use the output/lifecycle mutex. The
monitor waits on a separate lifecycle condition and claims a one-printer gate
when burnout is detected, so it does not compete with the scheduler mutex or a
queue of active printers. Each awakened requester re-runs scheduling before it
waits, preventing an elapsed cooldown from becoming a lost wake-up.

The implementation accepts zero for activity and cooldown durations, but
requires positive coder count, burnout time, and compile goal. A compilation is
counted after its compile interval completes. A coder that reaches its goal is
no longer eligible to burn out. With one coder, the sole dongle is taken once
and the monitor reports burnout because a pair can never be acquired.

## Exact submission inventory

```text
Makefile
README.md
include/codexion.h
src/coder.c
src/dongle.c
src/heap.c
src/heap_remove.c
src/init.c
src/log.c
src/main.c
src/monitor.c
src/parse.c
src/request.c
src/run.c
src/scheduler.c
src/time.c
```

Private checks belong in `tests/`; the subject remains in `resources/`.

## Validation

Run from `submission/`:

```sh
make
norminette include src
../tests/test.sh
```

Validated on 2026-08-30 with a clean `-Wall -Wextra -Werror -pthread` build,
Norminette, invalid-input checks, FIFO/EDF completion cases, one-coder burnout,
serialized-output checks, compile-duration and dongle-cooldown checks, leak
checks, and repeated EDF liveness runs. The five-coder case passed 100/100 and
the tight six-coder case passed 300/300 in the final local run. Paced monitor
checks stayed inside the subject's 10 ms window at 200, 500, and 1000 coders;
synthetic back-to-back creation of hundreds of thousands of threads can still
produce host-scheduling outliers, as anticipated by the subject's hardware/OS
tolerance note.
