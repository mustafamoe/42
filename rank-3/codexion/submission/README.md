*This project has been created as part of the 42 curriculum by mal-hall.*

# Codexion

## Description

Codexion simulates coders sharing pairs of USB dongles with mandatory cooldowns.
Each coder has a thread; a separate monitor detects burnout. Custom binary
heaps arbitrate contested dongles using FIFO or Earliest Deadline First (EDF).

## Instructions

```sh
make
./codexion number_of_coders time_to_burnout time_to_compile \
  time_to_debug time_to_refactor number_of_compiles_required \
  dongle_cooldown scheduler
```

All times are milliseconds. `scheduler` must be `fifo` or `edf`. Coder count,
burnout time, and compile goal must be positive; other durations may be zero.
The simulation ends at burnout or after every coder has completed the required
number of compiles. Coders continue their cycles until that global stop, so an
individual may compile more than the minimum.

## Resources

- The Codexion subject, version 1.5.
- POSIX pthread documentation: mutexes, condition variables, thread creation,
  and joining.
- Binary min-heap insertion, root removal, and comparator invariants.
- AI assisted with subject analysis, implementation and documentation drafts,
  concurrency review, simplification, and private regression tests.

## Blocking cases handled

A coder queues one request in each adjacent dongle heap. It can take the pair
only when it is first in both heaps and both dongles are free and cooled down.
There are no priority bypasses. FIFO compares enqueue sequence numbers; EDF
compares burnout deadlines, then sequence numbers and coder IDs for ties.

The pair is reserved atomically, breaking Coffman's hold-and-wait condition.
Both queues use the same total order, preventing circular queue dependencies.
Dongle mutexes are acquired in ascending index order to prevent mutex cycles.

Initial requests are queued by alternating seats: odd IDs, then even IDs.
For odd-sized rings, initial attempts are also staggered across compile and
cooldown time. This spreads competing requests instead of starting two rigid
waves. Subsequent requests are made immediately after refactoring and retain
the required FIFO/EDF ordering.

Release starts cooldown while the state and dongle mutexes are held and wakes
waiting coders. A blocked coder either waits for a release or timed-waits until
both cooldowns end. The wait uses the same availability result as the
acquisition check, avoiding a missed cooldown expiration. Timed waits finish
with short sleeps near the deadline to reduce OS timer-coalescing delays.

The monitor independently waits for the nearest burnout deadline. Every log
and compile completion also checks deadlines under the lifecycle mutex before
changing state. An expired coder cannot reset its timer or complete the goal
after burnout. Only the monitor prints the burnout message and stops workers.
One coder takes the sole dongle once and waits for burnout.

## Thread synchronization mechanisms

`state_lock` protects queues, pair acquisition, compile counts, and startup.
Each dongle also has its own mutex protecting ownership and cooldown. The
shared `changed` condition wakes workers at startup, release, and shutdown;
absolute timed waits handle activity durations and cooldowns.

`output_lock` protects compile-start timestamps, deadline checks, and a print
gate. A printer claims the gate under the mutex, then releases the mutex during
output. Other printers wait on `print_ready`, while the monitor can still
inspect deadlines. The `life_changed` condition wakes the monitor after a
compile start, completion, or detected burnout.

For example, a compile start checks all deadlines and resets its timestamp
under the same mutex. If a deadline has expired, new ordinary logs are blocked.
The monitor waits for the current print batch, prints one burnout line, then
wakes workers to stop. A compile batch contains two dongle lines and one compile
line. Lock nesting is always state before output or dongle locks; the monitor
releases output before acquiring state during shutdown.
