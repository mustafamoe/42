*This project has been created as part of the 42 curriculum by mal-hall.*

# Codexion

## Description

Codexion simulates coders sharing pairs of USB dongles with mandatory cooldowns.
One thread runs each coder; a monitor detects burnout. Custom binary heaps
schedule requests using FIFO or Earliest Deadline First (EDF).

## Instructions

```sh
make
./codexion number_of_coders time_to_burnout time_to_compile \
  time_to_debug time_to_refactor number_of_compiles_required \
  dongle_cooldown scheduler
```

Times are integer milliseconds. Coder count, burnout time, and compile goal
must be positive; other durations may be zero. Use `fifo` or `edf`.
Stop occurs at burnout or when every coder completes the goal. Until then,
coders keep cycling, so some may compile more than the minimum.

## Resources

- Codexion subject, version 1.5, and peer-evaluation checklist.
- POSIX [mutexes](https://pubs.opengroup.org/onlinepubs/9799919799/functions/pthread_mutex_lock.html) and [condition variables](https://pubs.opengroup.org/onlinepubs/9799919799/functions/pthread_cond_clockwait.html).
- Princeton Algorithms: [binary heaps](https://algs4.cs.princeton.edu/24pq/).
- AI assisted with subject analysis, C implementation, concurrency review,
  private regression tests, and documentation.

## Blocking cases handled

- **Deadlock:** reserve both dongles together, breaking Coffman's hold-and-wait
  condition. Both heaps share one ordering; mutexes lock by ascending index.
- **Starvation:** a coder must lead both heaps. FIFO orders by arrival sequence;
  EDF by deadline, then sequence and ID. No bypasses. Initial requests use odd
  IDs before even IDs; odd-sized rings also stagger initial attempts.
- **Cooldown:** release sets `ready_at`. Workers wait for release or cooldown
  expiry, then recheck availability. Short sleeps finish waits near deadlines.
- **Burnout:** the monitor checks deadlines; logs and compile completion check
  them too. An expired timer cannot be reset. One coder takes its sole dongle
  once and waits for burnout. The burnout line is printed once and last.

## Thread synchronization mechanisms

- `pthread_create` starts workers and the monitor. `pthread_join` waits for
  their exit before mutexes, conditions, and allocated memory are cleaned up.
- `state_lock` protects heaps, pair transitions, counts, and startup.
  Each dongle's `lock` protects `held` and `ready_at`. Nested locks take state
  before output or dongles; the monitor drops output before taking state.
- `output_lock` makes deadline checks and compile-start timestamp updates atomic.
  It also protects the print gate. Printing releases the mutex while retaining
  the gate, so the monitor can check deadlines. Two dongle lines and one compile
  line form one print batch, preventing interleaved logs.
- `pthread_cond_wait` releases its mutex while waiting and reacquires it before
  returning; loops recheck state after waking. Timed waits handle durations
  and cooldowns. `changed` wakes workers, `life_changed` wakes the monitor,
  and `print_ready` wakes printers. Signals and broadcasts announce changes.
