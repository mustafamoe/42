*This project has been created as part of the 42 curriculum by mal-hall.*

# Codexion

## Description

Codexion simulates coders sharing pairs of cooling dongles. Each coder runs in
its own thread, while a dedicated monitor detects burnout. A custom binary heap
on every dongle orders pair requests by FIFO arrival or earliest burnout
deadline.

## Instructions

Build and run:

```sh
make
./codexion number_of_coders time_to_burnout time_to_compile \
  time_to_debug time_to_refactor number_of_compiles_required \
  dongle_cooldown scheduler
```

All times are milliseconds. `scheduler` must be `fifo` or `edf`.

## Resources

The project subject, the POSIX documentation for pthread mutexes and condition
variables, and standard binary-heap references were used. AI-assisted tools
helped extract requirements, draft code and documentation, reason about
scheduling edge cases, and prepare tests. Every resulting part was reviewed
against the subject and kept small enough to explain directly.

## Blocking cases handled

A request is inserted into both adjacent dongle heaps with one immutable
priority. Both dongles are granted atomically, so a coder never holds one while
waiting for the other. This removes Coffman's hold-and-wait condition. Dongle
mutexes are also taken by index, so their own lock order cannot form a cycle.

Only requests whose complete pair is physically available are eligible for an
immediate grant. The best pending request receives a reservation barrier. At
most one eligible overlapping request may bypass it before that barrier is
enforced; under EDF, that bypass is allowed only when its compile and cooldown
finish by the protected request's deadline. Eligible requests on disjoint pairs
may still run. This avoids queue convoys, preserves parallel compiles, and puts
a fixed bound on interference so a request cannot be bypassed forever.

FIFO uses a monotonic arrival number. EDF uses the coder's burnout deadline,
then arrival order and coder ID as deterministic tie-breakers. Released dongles
store the exact end of their cooldown; a condition-variable timed wait prevents
reuse before that instant. Every awakened requester asks the scheduler to
re-evaluate before sleeping again, so an elapsed cooldown cannot become a lost
wake-up.

All coder threads reach a startup barrier before the simulation clock begins.
Initial arbitration is prepared before that clock, then initial compile starts
are released in a short chain. A dedicated monitor waits independently for the
nearest burnout deadline. A priority print gate lets a detected burnout claim
the next complete output line before queued coder messages. Invalid arguments,
one coder, zero-duration activities, thread-creation failure, burnout, and
successful completion are also handled.

## Thread synchronization mechanisms

A simulation mutex protects all heaps, grants, request deadlines, compile
counts, and the stop state. Each coder has a condition variable, allowing the
scheduler to wake the exact coder whose request was granted or whose cooldown
must be reconsidered. A shared condition variable handles startup, timed phase
waits, and shutdown. Each dongle has its own mutex protecting its held state and
cooldown timestamp. Pair locks are taken in ascending index order.

For example, a coder queues the same request on both dongles while holding the
simulation mutex. The scheduler locks both dongles, removes that request from
both heaps, and changes both held states as one transaction. The coder records
its compile start at the same timestamp as its serialized compile message. A
lifecycle condition immediately wakes the monitor whenever that timestamp or a
completion state changes.

The output mutex protects lifecycle data and a one-printer gate. Coders wait on
that gate instead of forming a long queue while printing. At a deadline, the
monitor marks death pending, waits for at most the current complete message,
prints the burnout line, and wakes all workers to stop. This prevents mixed
lines and prevents coder messages after burnout.
