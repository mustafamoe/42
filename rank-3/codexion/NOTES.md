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

## Defense review, 2026-09-27: read this before the older checklist

The checklist and validation above describe the previous implementation work;
they are not a fresh guarantee of submission readiness. This teaching review
read all 13 C files, the header, Makefile, README, private test script, and all
16 pages of subject version 1.5. No evaluation sheet is supplied locally.
The source was not changed during this review.

The existing private test script passes with the installed Command Line Tools:

```sh
DEVELOPER_DIR=/Library/Developer/CommandLineTools sh rank-3/codexion/tests/test.sh
```

Run this command from the workspace root. Plain `make` currently encounters
a host toolchain mismatch: Xcode clang 17's linker reads a macOS 27 SDK with
an architecture it does not understand. The environment override selects the
matching installed Command Line Tools. It does not modify the Makefile or
system configuration. Norminette was not available on PATH during this review;
its earlier pass was not revalidated. Leak/race sanitizers were not rerun.

### Submission concerns established during this review

1. **The implemented arbitration is not strict per-dongle FIFO/EDF.**
   Subject printed pages 8 and 12 require arrival/deadline order for a contested
   dongle. `best_eligible()` scans entries below heap roots, and
   `next_candidate()` permits an overlapping bypass. With four initial FIFO
   requests in ID order, the scheduler grants coders 1 and 3 while coder 2
   waits. Coder 2 requested dongle index 2 before coder 3. An isolated probe
   produced grants `1 0 1 0` and `coder2.bypassed = 1`. This is a deliberate
   implementation deviation, not something a heap or a README makes compliant.
   Pair coordination and the subject's EDF liveness requirement need to be
   reconciled before claiming full compliance. No conflicting official
   evaluation sheet was found; the conflict here is between code and subject.
2. **Cooldown is timestamped before the release critical section.**
   `release_dongles()` computes `now_ms() + cooldown` before acquiring
   `state_lock`. Waiting for that lock consumes some or all of the cooldown
   while the dongles remain held. A probe held `state_lock` for about 100 ms
   while another thread called release with a 20 ms cooldown. At the earliest
   actual release, `ready_at` was already 85 ms in the past. Timestamping at
   the synchronized release transition is the correction to reason about.
3. **A late compile can overwrite an expired burnout timestamp.**
   `begin_log()` checks `stopped` and `death_pending`, but does not check
   `now >= last_compile + burnout` before replacing `last_compile`.
   `pair_ready()` checking an earlier scheduling time is insufficient:
   a granted worker can be delayed before reaching the print gate.
   An isolated function probe passed an age of 100 ms with burnout 50 ms;
   `log_compile()` accepted it and reset the timestamp. This establishes the
   missing guard, not a measurement of its frequency in normal runs. In an
   actual execution, a delayed monitor and a worker winning `output_lock`
   can allow that reset before detection. The compile-start transition must
   reject an already-expired deadline under the lifecycle lock and coordinate
   detection with the monitor.

Other limitations to understand: the completion transition has no independent
deadline check either; it relies on the monitor winning in time. Completed
coders retire individually and are exempted from burnout, an interpretation
not explicitly spelled out by the subject. An EDF bypass estimate uses
scheduler time, not actual compile start, so its 10 ms margin is a heuristic,
not a proof. Wall-clock jumps and arbitrarily delayed stdout/OS scheduling
also prevent a hard real-time guarantee. The README's claim that death waits
for at most one message is imprecise: a compile log holds the gate across
three `printf` calls.

## Technical defense guide

### 1. What the program actually simulates

There is one process, N coder threads, one monitor thread, and the main thread.
Thus a successful run creates N+1 pthreads and has N+2 threads including main.
All share the same address space; each has its own execution context and stack.
The simulation does not actually compile source code. Compilation, debugging,
and refactoring are timed phases with logged transitions.

There are N dongles in a ring. Coder array index `i` has displayed ID `i+1`,
left dongle `i`, and right dongle `(i+1)%N`. With four coders:

```text
coder 1 -> dongles 0,1
coder 2 -> dongles 1,2
coder 3 -> dongles 2,3
coder 4 -> dongles 3,0
```

Adjacent coders conflict; coders 1 and 3 can compile simultaneously. For N>=2,
at most floor(N/2) coders can compile simultaneously, since each holds two
distinct dongles. For N=1, the two computed indices refer to the same object;
one dongle does not constitute a pair, so the coder can never compile.

Say this in a defense: "I model each coder as a pthread. A shared scheduler
reserves both adjacent dongles together. Dongle flags represent ownership;
mutexes protect state transitions. A separate monitor watches compile-start
deadlines, and condition variables let workers sleep until useful events."

### 2. Arguments, units, and the timing contract

```sh
./codexion 5 800 30 10 10 3 5 edf
```

| Position | Field | Meaning in the example |
| --- | --- | --- |
| 1 | `coders` | 5 coders and 5 dongles |
| 2 | `burnout` | 800 ms allowed between compile starts |
| 3 | `compile` | Hold a pair during a 30 ms compile |
| 4 | `debug` | Debug for 10 ms |
| 5 | `refactor` | Refactor for 10 ms, then request again |
| 6 | `goal` | Each coder must finish 3 compiles |
| 7 | `cooldown` | Released dongles wait 5 ms before reuse |
| 8 | `policy` | Earliest Deadline First |

The program requires `argc == 9`: eight arguments plus `argv[0]`.
Only nonempty strings of ASCII decimal digits are accepted for numbers.
Leading zeros are accepted; signs, whitespace, decimal points, and suffixes
are rejected. Every numeric input is capped at `INT_MAX`. Coder count,
burnout, and goal must be positive. Compile/debug/refactor/cooldown may be 0.
Policy matching is exact and case-sensitive.

The burnout deadline is:

```text
deadline = last_compile_start + time_to_burnout
burnout  = now >= deadline, for a coder not marked done
```

Before the first compile, `last_compile` is initialized to the simulation
start. Beginning a compile resets the timer; finishing does not. A coder can
therefore burn out while compiling, debugging, refactoring, or waiting. If a
compile starts at elapsed 100 ms and burnout is 250 ms, the next deadline is
350 ms even if that compile has not finished by then.

For repeated compilation, the interval between starts includes compile,
debug, refactor, resource waiting, and scheduling overhead. Comparing burnout
only against compile time is insufficient. Resource capacity and ring
conflicts also matter; a simple sum is not a complete feasibility proof.

### 3. Codebase map and reading order

| File | Responsibility |
| --- | --- |
| `include/codexion.h` | Types, shared state, public function declarations |
| `src/main.c` | Parse, initialize, run, clean up, report failure |
| `src/parse.c` | Strict input validation and policy selection |
| `src/init.c` | Allocation, primitive initialization, partial cleanup |
| `src/run.c` | Thread creation, startup barrier, initial requests, joins |
| `src/coder.c` | Coder lifecycle and compile completion counting |
| `src/request.c` | Enqueue requests and wait for grants/cooldowns |
| `src/scheduler.c` | Choose pending/eligible requests and grant pairs |
| `src/dongle.c` | Pair locks, readiness, release/cooldown state |
| `src/heap.c` | Comparator, heap insertion, heap root lookup |
| `src/heap_remove.c` | Remove a particular request and repair the heap |
| `src/time.c` | Milliseconds, absolute waits, wake/stop helpers |
| `src/log.c` | Printing gate and compile-start timestamp transition |
| `src/monitor.c` | Startup handshake, deadline detection, burnout shutdown |
| `Makefile` | Compilation, linking, incremental rebuilds, cleanup |
| `README.md` | Required user-facing usage and synchronization explanation |

Read header, main, parse, init, run, coder first; then follow request ->
scheduler -> heap/dongle. Finish with time, logging, and monitor. These last
three explain how an otherwise correct resource algorithm can still fail
on timing or shutdown.

### 4. Every data structure and its ownership

`t_policy` is the FIFO/EDF enumeration. `t_config` contains immutable parsed
configuration. `t_cond` is only an alias for `pthread_cond_t`, not a custom
event implementation.

`t_heap` contains `t_coder **data` and `size`. This is an array of pointers to
existing coder objects, not copied coders and not individually allocated
requests. Each dongle allocates exactly two pointer slots, because at most
its two adjacent coders can request it. A coder has at most one outstanding
request and is inserted only once per distinct dongle. Those invariants make
the fixed capacity safe; `heap_push()` itself has no capacity check.

`t_dongle` contains:

| Field | Purpose |
| --- | --- |
| `lock` | Protect access to physical availability fields |
| `held` | Logical reservation, maintained across the compile interval |
| `ready_at` | Absolute millisecond time when cooldown ends |
| `queue` | Requests needing this dongle; protected by `state_lock` |

The mutex is not the reservation. The scheduler briefly locks it, sets
`held=1`, and unlocks it. The coder keeps logical ownership until release.
This avoids holding an operating-system mutex throughout a simulated phase
and lets the scheduler inspect availability. It also avoids having one thread
unlock a mutex acquired by a different thread.

`t_coder` contains:

| Fields | Purpose |
| --- | --- |
| `id`, `left`, `right` | Display ID and ring resource indices |
| `compiles` | Number of fully completed compile intervals |
| `done` | Retired after reaching the goal; monitor ignores it |
| `requesting` | Its request is in the relevant heap(s) |
| `granted` | Pair reserved; worker has not consumed the grant yet |
| `activated` | Worker is allowed through its startup wait |
| `bypassed` | Overlap barrier armed for this pending request |
| `last_compile` | Actual recorded compile-start absolute time |
| `deadline` | Immutable priority snapshot while a request is queued |
| `sequence` | Shared monotonic request number, assigned under state lock |
| `thread`, `ready` | Worker handle and personal condition variable |
| `sim` | Pointer back to shared simulation state |

`granted` becomes 0 when the worker consumes its grant, even though it still
owns the dongles. Do not use `granted` as a general "currently compiling"
flag. `activated` stays true after first activation. `requesting` distinguishes
a queued coder from one with a grant or doing another phase.

Two deadline values are intentional. A queued priority must not change while
inside the heap. The monitor uses live `last_compile + burnout`, while the
scheduler uses the saved request `deadline`. A coder cannot start a new
compile while its old request is still pending.

`t_sim` owns the arrays and all shared coordination. Its fields group as:

- `config`, `coders`, `dongles`: configuration and owned storage.
- `state_lock`, `output_lock`: scheduling and lifecycle/printing locks.
- `changed`, `life_changed`, `print_ready`: shared condition variables.
- `monitor`: the separate monitor handle.
- `start`, `next_sequence`: common time origin and request sequence source.
- `started`, `workers_ready`, `monitor_ready`, `monitor_armed`: startup state.
- `stopped`: terminal simulation state.
- `death_pending`: prohibit new ordinary print batches once death is detected.
- `printing`: exactly one print batch currently owns the output gate.
- `completed`: number of retired coders, not total compile count.
- `threads_created`, `monitor_created`: which thread handles can be joined.
- `state_ready`, `output_ready`, `cond_ready`, `life_cond_ready`,
  `print_cond_ready`, `dongles_ready`, `coder_conds_ready`: which initialized
  synchronization objects can safely be destroyed after partial failure.

### 5. Parsing, initialization, and C details

`main()` keeps `config` and `sim` on its stack. Their lifetime lasts through
all thread joins. Each pthread receives a pointer to a stable coder array
element, not the address of a loop variable. That prevents the common bug
where all threads accidentally receive the same changing `i`.

The main path is `parse_args -> init_sim -> run_simulation -> cleanup_sim`.
Argument/init/thread-creation failure writes `Error\n` to file descriptor 2
and returns 1. A simulated burnout is a successfully executed simulation;
the existing code returns 0 for it.

`parse_number()` calculates a decimal value as `value*10 + digit`. It checks
first that `value <= (INT_MAX-digit)/10`; this algebraic rearrangement prevents
overflow before performing the multiplication. A `long long` accumulator
does not remove the need to enforce the intended input bound. `parse_policy()`
maps two exact strings to enum values. `parse_args()` fills the seven numeric
fields, checks the three positive requirements, then validates the policy.

`init_sim()` zeroes the whole simulation, copies configuration, and calls:

1. `init_locks()`: two mutexes and three shared condition variables.
2. `init_dongles()`: an N-element array; two queue pointer slots and one mutex
   for every dongle.
3. `init_coders()`: an N-element array, IDs/indices/back-pointers, and N personal
   condition variables.

`memset` zeroes bookkeeping and pointers; it does not replace pthread init.
Flags are set only after successful initialization. If any step fails,
`cleanup_sim()` destroys only initialized primitives and frees allocations.
The dongle array was zeroed, so future/unallocated queue pointers are NULL and
safe to pass to `free`. If a queue allocation succeeds but mutex init fails,
that allocation is still freed without destroying the uninitialized mutex.

On normal shutdown, cleanup happens after every created thread is joined.
Freeing coder storage while threads still use their pointers would be a
use-after-free. Destroying a condition/mutex still in use is also invalid.

C syntax worth explaining:

- File-scope `static` functions have internal linkage; they are private helpers,
  not global state. `static` on a function is not a static local variable.
- `typedef struct s_sim t_sim;` allows mutually referring structures via pointers
  before the full structure definition is known.
- `coder->sim` dereferences a structure pointer; `&sim->state_lock` passes an
  object's address. `t_coder **` lets a swap function replace pointer slots.
- `void *(*)(void *)` is the pthread start-function shape. Returning NULL ends
  that worker function; `pthread_join` waits for it.
- `return (write(...), 1)` uses the comma operator: execute the left expression,
  then return the right expression. It does not return two values.
- `while (compile_cycle(coder)) ;` intentionally has an empty loop body; the
  work is performed in the condition call.
- Header guards prevent duplicate declarations during preprocessing. Prototypes
  enable checked calls across C translation units. Includes do not imply that
  every available library function is authorized or actually called.

### 6. Startup and thread lifecycle: run.c

`create_threads()` creates all workers, updating `threads_created` after each
success, and then creates the monitor. `start_threads()` holds `state_lock`
and waits until all created workers have incremented `workers_ready` and the
monitor has set `monitor_ready`. Condition waiting releases the lock, so those
threads can actually report readiness.

Before setting the start time, `queue_initial_requests()` inserts requests in
coder ID order. Their temporary deadlines are all `LLONG_MAX`, ensuring equal
EDF priorities during setup. It calls the scheduler to reserve initial pairs.
Then `start_threads()` establishes one common `start`, initializes every
`last_compile` and deadline, sets `started`, and broadcasts `changed`.
Updating all initial deadlines to the same value preserves heap ordering:
sequence remains the tie-breaker. Arbitrarily changing queued keys later
would not have that property.

The worker's startup predicate requires `started && monitor_armed && activated`,
unless stopped. `arm_monitor()` sets `monitor_armed` and signals activated
workers, including at most one initial granted worker in that loop.
`log_compile()` subsequently signals the next outstanding grant, forming an
intended startup signal chain. This reduces a simultaneous wakeup burst;
spurious wakes and later scheduler signals mean it is not a strict execution
ordering guarantee. Initial scheduling is prepared before time zero, but
recorded compile starts occur afterward.

If creation fails, `start_threads(..., failed=1)` skips the readiness wait,
sets startup state, calls `stop_workers()` and wakes waiters. `join_threads()`
joins only successfully created handles. `run_simulation()` returns the thread
creation result, so main can report a setup error after cleanup.

### 7. One coder's complete execution: coder.c

`coder_thread()` reports startup readiness and waits on its own `ready`
condition. After startup it repeats `compile_cycle()` until it returns 0.

For N>=2 a cycle is:

```text
request pair
  -> wait for grant
  -> record compile start and print two takes + compiling
  -> wait until last_compile + compile_duration
  -> release pair / begin cooldown
  -> count completed compile
       -> if goal reached, retire
       -> otherwise debug, then refactor, then repeat
```

`use_dongles()` dispatches to `log_compile()` for a real pair. For one coder,
it prints a single take and waits on `changed` until the monitor stops the
simulation. It does not attempt to lock the same mutex twice or pretend it
has two distinct resources.

If logging or the compile wait is interrupted, `compile_cycle()` releases
its granted resources before returning. `release_dongles()` runs before
`finish_compile()`. `finish_compile()` takes state then output lock, refuses
to count once stop/death is pending, invokes `record_compile()` otherwise,
and notifies the monitor. `record_compile()` increments `compiles`, marks
goal-reaching coders done, increments `completed`, and sets stopped when
`completed == config.coders`.

There is no debug/refactor phase after a coder's final required compile.
`compiles` counts finished work, whereas an `is compiling` line counts starts;
these differ when burnout interrupts a compile. Tests must not confuse them.
Debug and refactor waits use `now_ms()+duration` after logging, so logging
overhead is not subtracted from those intervals.

### 8. Requests and cooldown wakeups: request.c and dongle.c

`request_dongles()` holds `state_lock`. It returns false immediately if stopped.
It only calls `add_request()` if the coder is neither requesting nor already
granted, because startup may have queued or granted it already.

`add_request()` snapshots `last_compile + burnout` while holding `output_lock`,
assigns a sequence under `state_lock`, resets bypass state, and inserts the
same coder pointer into both relevant queues (only once for N=1).
`requests_overlap()` compares both pairs of indices to detect any shared dongle.

After asking the scheduler to run, a worker loops until granted or stopped.
`wait_for_schedule()` calls `next_schedule_time()`, which finds the earliest
future `ready_at` among all unheld dongles. If one exists it timed-waits on
the coder condition until that absolute time; otherwise it waits without
a timeout. Every return from that wait reruns scheduling. A wakeup is only
a request to re-check state; it is not a grant.

Why timed waits? A cooldown expiring is passage of time, not a thread that
will automatically emit a signal. Why schedule before sleeping and after
waking? To evaluate grants against current state instead of depending on a
signal that may have happened before the worker began waiting.

`pair_mutex()` orders two locks by ascending dongle index. When both indices
are equal, it takes/releases the single mutex once. It unlocks in ascending
order too; reverse unlock order is conventional but not required for this
usage. `pair_ready()` rejects an expired request, locks both dongles, and
checks `!held` plus `ready_at <= now` for each.

`free_dongle()` updates held/cooldown under that dongle's mutex.
`release_dongles()` holds state while freeing the two dongles and scheduling
new requests, so no scheduler can observe a half-released pair. Its current
timestamp-before-state-lock issue is documented above.

### 9. Binary heaps and exact complexity

A min-heap has the invariant that a parent is never lower priority than its
children. Only the root is guaranteed globally best; the entire array is not
sorted. With zero-based indexing:

```text
parent(i) = (i-1)/2, for i>0
left(i)   = 2*i+1
right(i)  = 2*i+2
```

`request_before(a,b,policy)` compares:

- FIFO: sequence first, then ID if equal.
- EDF: deadline first, sequence second, ID last.

IDs are a deterministic final fallback; sequences are normally distinct.
FIFO arrival here means scheduler enqueue order under `state_lock`, not which
thread the OS created first. Initial enqueue order is explicitly ID order.
Equal EDF deadlines occur naturally at startup and with millisecond precision.

`heap_push()` appends the pointer and swaps upward until the parent is already
ordered. `heap_peek()` returns NULL for an empty heap or the root otherwise.
`heap_remove()` searches by pointer identity, decrements size, and, unless the
target was last, replaces it with the old last element. `move_up()` repairs
against ancestors; `move_down()` repairs against the better of the two children.
Arbitrary removal is needed because a granted pair-ready request may be below
a heap root. Each source file's `swap_coders()` just exchanges pointer slots.

For a hypothetical heap size k: insertion is O(log k), peek O(1), and this
removal is O(k) search plus O(log k) repair, hence O(k), not O(log k) overall.
Here k<=2, so each individual heap operation is effectively constant time.

The scheduler still scans N dongles and up to 2N queue entries. Each candidate
selection is O(N); a scheduling call can grant O(N) requests, so its worst-case
work is O(N^2). A monitor scan and cooldown scan are O(N). Explicit arrays and
queue storage are O(N), plus O(N) OS thread resources. Having heaps does not
make the whole scheduler O(log N).

### 10. The scheduler, function by function

The scheduler is a set of functions called by workers and main; it has no
dedicated scheduler thread. All callers hold `state_lock`.

`best_pending()` inspects every heap root and chooses the best request among
them. The global best pending request must be a root somewhere: no better
request can hide below a worse root in a valid min-heap with the same comparator.
Pointers appear in two heaps, but seeing duplicates does not change the minimum.

`best_eligible(sim, protect, now)` scans every queued entry and selects the
best request whose complete pair is physically available and whose deadline
has not expired. If `protect` is set, it excludes every candidate sharing a
dongle with that protected request. It deliberately scans beyond heap roots.

`grant_request()` locks the pair, removes the coder from both queues, sets both
held flags, clears requesting, sets granted/activated, and signals that coder.
Its updates form one scheduling transaction because state remains locked.
A signal does not mean the worker runs immediately.

`next_candidate()` implements the reservation barrier:

1. If the best pending request was already bypassed, allow only disjoint pairs.
2. Otherwise find the best physically eligible request.
3. If it is disjoint from the priority request, allow it without using a bypass.
4. If it overlaps, FIFO allows it and marks the priority request bypassed.
5. EDF allows that overlap only if
   `now + compile + cooldown + 10 < priority->deadline`.
   When the test fails, it marks the barrier armed and looks for a disjoint pair.

Thus `bypassed=1` can mean an overlapping grant happened OR EDF refused an
unsafe overlap and armed protection. It is not a precise numerical counter.
The literal 10 is a conservative timing margin, not the required burnout
reporting tolerance being enforced by the monitor, and not a proven bound on
thread or output delay.

`schedule_requests()` samples `now` once. It repeatedly grants the global
best request while that request is pair-ready. When the best request is
blocked, it holds that request as the priority barrier and grants candidates
chosen by `next_candidate()`. It finally activates/signals the protected worker
so that it can participate in cooldown waiting. A single captured `now` may
become stale during a long scan, another reason actual compile start must check
its own timing invariant.

Trace with four initial FIFO requests:

```text
grant coder 1: owns 0,1
coder 2 is oldest pending: needs 1,2, blocked on 1
coder 3: needs 2,3, physically available
grant coder 3 once; mark coder 2 protected
further overlapping bypasses of coder 2 are blocked
```

The intent is concurrency with bounded interference. It avoids one blocked
request forcing all disjoint work to idle. But it also shows exactly why
strict per-dongle FIFO is not currently obeyed. Never present this as identical
to serving the root of each dongle queue.

Bounded bypass is not by itself a proof that every feasible EDF workload meets
its deadlines. In particular, later requests can have earlier EDF deadlines,
OS scheduling has no hard upper bound here, and grant time differs from compile
start. Liveness, deadline feasibility, and fairness are separate properties.

### 11. Mutexes, condition variables, and lock order

A data race is unsynchronized conflicting access to memory where at least one
access writes. In C it can cause undefined behavior. A mutex provides mutual
exclusion and synchronization for the memory protected by that protocol.
`volatile` is not a replacement for mutexes.

Use this ownership table rather than saying "the global mutex protects all":

| State | Synchronization during active simulation |
| --- | --- |
| Heaps, sequence, requesting/granted/activated/bypassed, request deadline | `state_lock` |
| Dongle held/ready_at | Dongle lock, with state lock around scheduling transitions |
| last_compile, done, print gate, death_pending | `output_lock` |
| compiles/completed | Updated by completion under state then output |
| stopped | Writes hold both state and output; readers hold at least one |
| Immutable config/indices/pointers and published start | Established before use through startup synchronization |

Initialization before publication is not a concurrent write. A worker reads
its own `last_compile` after recording it; only that worker updates that value
after startup, while monitor reads use output lock.

Nested lock directions are state -> output and state -> dongle(s), with pair
mutexes ascending. Code must not hold output while acquiring state. The monitor
deliberately releases output before taking state during burnout shutdown;
`log_compile()` likewise finishes the print gate before taking state to wake
another worker. Reversing that order against a worker taking state then output
could deadlock.

`pthread_cond_wait(cond, mutex)` is called with the mutex held. It atomically
releases it while waiting and reacquires it before returning. The associated
predicate must be checked in a `while` loop because of spurious wakes and
state changes by other threads before lock reacquisition.

Condition variables do not store a durable notification. The durable facts
are flags such as granted and stopped. `signal` wakes at least one waiter;
`broadcast` wakes all current waiters. Neither hands ownership of a resource
to a thread. State protected by the mutex does that.

| Condition | Associated mutex | What changes can wake it |
| --- | --- | --- |
| `coder.ready` | state | Activation, grant, cooldown timeout, stop |
| `changed` | state | Startup readiness/start, phase timeout, stop |
| `life_changed` | output | Compile-start reset, completion, print end during death, stop, deadline timeout |
| `print_ready` | output | Print gate becomes free or shutdown blocks new logs |

`wait_until()` computes one absolute timeout, then loops until stopped or time
reached. An unrelated signal does not restart the duration. `make_timespec()`
converts milliseconds to seconds plus nanoseconds; timedwait expects an
absolute deadline, not "sleep this many milliseconds."

`now_ms()` uses epoch milliseconds from `gettimeofday`: seconds*1000 plus
microseconds/1000. The cast before multiplication prevents a narrow
intermediate. Logging subtracts `sim.start`. These are wall-clock timestamps,
not CPU time or monotonic time. They align with default realtime condition
timeouts, but system clock adjustments can distort simulated intervals.
Do not switch only `now_ms()` to a different clock and leave timed waits in
the old clock domain.

### 12. Printing without holding the output mutex across printf

`begin_log()` takes output lock, waits while printing is busy, and refuses new
ordinary messages after stop or death pending. It samples the timestamp and,
for a compile, updates last_compile and signals the monitor. It sets printing
and unlocks. The caller prints while logically owning the gate.

`end_log()` takes output lock, clears printing, and either wakes the monitor
if death is pending or wakes another printer. The mutex protects the gate;
the gate preserves exclusivity even while the mutex is unlocked for I/O.
This allows the monitor to inspect lifecycle state while a printer is in printf.

`log_event()` prints one ordinary message. `log_compile()` prints two dongle
takes and one compile start with one captured timestamp, within a single gate
ownership period. These are emitted at the recorded start, not at the earlier
scheduler grant. After the batch it signals another pending grant.
`log_death()` formats the burnout line; its caller has already claimed the gate.

The death gate gives priority only after the monitor detects death and sets
death_pending. It does not prevent the earlier expired-deadline reset described
above. Nor does it bound how long an already active batch can spend in a blocked
stdout write. `printf` buffering also means a formatted line and externally
observed bytes are not always the same instant.

### 13. Monitoring and the two shutdown paths

After `arm_monitor()`, `monitor_thread()` transfers from state lock to output
lock. Its main loop uses output lock alone, avoiding the scheduler's state lock
while finding deadlines.

`find_dead_coder()` scans in ID order and returns the first unfinished expired
coder. If several are expired, this is not necessarily the earliest deadline;
it is the first expired array element. `first_deadline()` finds the nearest
future/next relevant deadline among unfinished coders. The monitor timed-waits
on life_changed until it or a lifecycle event occurs, then scans again.

Burnout shutdown in `burn_out()`:

1. With output held, set death_pending so no ordinary batch can enter.
2. Wait for the currently active batch, if any, to finish.
3. Claim printing, release output, and print exactly one burnout line.
4. Reacquire output, clear printing, wake gate waiters, and release output.
5. Take state then output, set stopped, notify lifecycle waiters, and release
   output; wake all workers and release state.
6. Return from the monitor. Main eventually joins all workers and the monitor.

During the brief gap before stopped, death_pending already rejects new logs
and compile completions. Some scheduling can still happen, but it cannot emit
new ordinary logs through that gate.

Successful completion instead occurs in record_compile when completed reaches
N. finish_compile notifies the monitor, wakes printers, and wakes workers.
`wake_workers()` signals each personal condition and broadcasts changed.
`stop_workers()` is the setup-failure helper; its caller already holds state,
and it takes output to set stopped before waking everyone.

The monitor is event/deadline driven, not a busy loop continuously burning CPU.
Still, a normal pthread scheduler cannot guarantee exact hard real-time
execution under every load. The subject's 10 ms requirement must be measured
under appropriate evaluation conditions, not asserted from code structure.

### 14. Deadlock, starvation, and livelock

Deadlock means a set of threads cannot progress because each waits for a
resource whose release depends on another in that set. The four Coffman
conditions are mutual exclusion, hold-and-wait, no preemption, and circular
wait. All four are needed for the classic resource deadlock situation.

For logical dongles, pair grants break hold-and-wait: a coder never reserves
one distinct dongle while waiting for its second. For implementation mutexes,
consistent lock order avoids circular wait. These are two related but separate
arguments; dongle pair grants do not excuse inverted state/output lock order.

Starvation means a particular coder is repeatedly denied progress while others
progress. A deadlock-free algorithm may still starve. FIFO order or EDF plus a
carefully justified fairness mechanism addresses a different concern from
mutual exclusion. This code's barrier intends to bound overlap while a request
is protected, but the overall EDF guarantee remains unproven.

Livelock means threads keep reacting without completing useful work, such as
two coders repeatedly taking/releasing a first dongle in synchronized retries.
Pair reservation and condition waits avoid that naive retry pattern.

### 15. Build, external calls, and submission inventory

The Makefile transforms each source name from `.c` to `.o`. `-Iinclude`
locates the header; `-c` compiles without linking. `$<` is the first prerequisite
and `$@` the target. All objects depend on codexion.h so header edits rebuild
them. The executable depends on the objects, preventing unnecessary relinking
when source/header modification times have not changed.

`-Wall -Wextra` enable warning groups, `-Werror` promotes warnings to errors,
and `-pthread` enables platform thread compilation/link behavior. These flags
do not prove absence of races or logical bugs. `clean` removes objects;
`fclean` also removes the binary; `re` requests both full cleanup and rebuild.
`.PHONY` prevents a file named clean/all/etc. from suppressing these recipes.
`make -j re` can race its independent prerequisites in this layout; ordinary
`make re` is the intended command.

External calls actually used fall into these groups: allocation/free/zeroing,
strcmp parsing, gettimeofday, write/printf, pthread creation/join, mutex
init/lock/unlock/destroy, and condition init/wait/timedwait/signal/broadcast/
destroy. These appear in the subject's permitted list. Not every permitted
function must be used; this implementation needs neither Libft nor atoi nor
usleep for its normal waits.

The allocation/init/create return values are checked. Many lock/wait/join
return values are not checked. Correct initialized normal mutex usage is
assumed, and wait predicates are rechecked; that does not amount to exhaustive
recovery from arbitrary pthread API failures.

Submit the contents of submission/: Makefile, README.md, header, and the 13
C files. NOTES.md, subject PDF, private tests, and the existing visualizer are
outside the evaluation content. Do not submit generated .o files or codexion.

### 16. What the current tests establish and miss

The checked-in shell script rebuilds, tests invalid policy/overflow, runs the
single-coder case, runs FIFO/EDF completion cases, two EDF liveness examples,
a compile-duration case, a neighbor cooldown case, a 200-coder short-deadline
case, and log-format validation. It fcleans after success. Its passing result
is useful evidence for those specific scenarios only.

Limitations worth explaining during defense:

- Completion checks mostly count compile-start messages, not an independent
  observation of completed work.
- Neighbor compile-start spacing is a useful cooldown proxy but cannot prove
  cooldown begins at the exact actual release instant under lock contention.
- There is no direct assertion of strict per-dongle FIFO/EDF order.
- A handful of EDF examples cannot establish liveness for every feasible case.
- The AWK checks that call `exit 1` in a main action and then unconditionally
  execute `END { exit ... }` can overwrite that earlier failure status. A robust
  checker should accumulate a failure flag and include it in its final exit.
- The script has no per-command timeout, so a deadlock could hang it.
- Regex-format checks do not by themselves prove resource exclusivity or
  absence of logs after a burnout line.

The isolated probes from this review were diagnostic, outside submission;
they force internal states/lock contention to examine specific invariants.
They do not substitute for end-to-end workload tests or a race detector.

### 17. Evaluator questions you should answer without guessing

1. **Why pthreads?** The subject requires one thread per coder. Threads share
   the simulation objects, making synchronization necessary.
2. **How many threads?** N workers plus one monitor, and main still exists.
3. **What is shared?** Heap/coder/dongle arrays and simulation coordination;
   function-local ordinary variables belong to each invocation.
4. **Why no globals?** The subject forbids them. A stack-owned sim is passed
   by pointer and remains alive until joins finish.
5. **When does burnout reset?** At the recorded start of a compile.
6. **Can a compiling coder burn out?** Yes, if it reaches its next deadline
   before another start; compiling itself does not suspend the timer.
7. **What is the difference between grant and compile start?** Grant reserves
   resources; the worker may run/log later. That delay matters for burnout.
8. **Why two queue entries?** A request needs both resources; both queues hold
   the same coder pointer, not two independent requests.
9. **Why capacity two?** A ring dongle has at most two neighboring requesters,
   each with at most one pending request.
10. **Why not change EDF priorities while queued?** That would invalidate the
    heap unless it is repaired. The request uses an immutable snapshot.
11. **Why sequence instead of arrival milliseconds?** It gives unambiguous
    enqueue order even when multiple requests share the same millisecond.
12. **What is EDF tie-breaking?** Deadline, then sequence, then ID.
13. **Do you always grant both heap roots?** No. Current code permits a bounded
    overlapping bypass; explain the exact subject-compliance concern.
14. **Does a heap make your scheduler logarithmic?** No. It scans queues and
    may repeat scans; worst-case one scheduling call is quadratic in N.
15. **Why a separate monitor?** A worker can be blocked; detection must still
    proceed independently of that worker's progress.
16. **Why conditions instead of usleep polling?** Event-driven wakeups plus
    timed waits reduce polling and allow shutdown to interrupt phase waits.
17. **Why while around wait?** The predicate can still be false after waking.
18. **Can a signal be lost?** A notification has no stored credit. Protected
    state/predicate checks preserve correctness when no waiter received it.
19. **What does a cond wait do to the mutex?** Atomically releases it for the
    wait, then reacquires it before returning.
20. **Are dongle mutexes held throughout compile?** No. Held flags persist;
    mutexes protect short accesses and transitions.
21. **Why lock index order?** Prevent a cycle among threads acquiring pairs.
22. **Why state then output?** One consistent nested lock direction avoids
    an ABBA deadlock with scheduler/completion paths.
23. **Why can printf run after unlocking output?** The protected printing
    flag acts as a one-owner gate; every printer follows that protocol.
24. **Why no output after burnout?** Death pending blocks new ordinary batches
    before the monitor claims the print gate.
25. **Can the death line wait?** Yes, for an active batch (possibly three lines)
    and for OS/I/O execution. The design is not hard real time.
26. **Why gettimeofday and long long?** Subject permits realtime; epoch
    milliseconds need wide arithmetic. Wall-clock adjustments are a limitation.
27. **Why join before cleanup?** Wait until no worker can access freed storage
    or destroyed synchronization objects.
28. **What if only some threads start?** Stop/wake the successfully created
    threads, join only those handles, then clean initialized resources.
29. **Why reject +5 if atoi accepts it?** The parser intentionally accepts
    digits only, avoiding loose conversions and ambiguous error reporting.
30. **Does a pass prove race freedom?** No. Tests sample executions; ownership
    reasoning and dedicated tools provide additional evidence.
31. **Is fairness the same as meeting deadlines?** No. Waiting a finite time
    can still exceed burnout; feasible EDF progress needs a stronger argument.
32. **What would you fix before submitting?** Strict policy compliance, the
    release timestamp boundary, expired lifecycle transitions, and test blind
    spots, followed by required style/build/concurrency checks.

### 18. Practice recodes and mastery checks

Use a temporary copy for exercises so the intended submission stays coherent.

1. Trace the first grants for N=1, N=2, N=4 and N=5 on paper. List queues,
   held flags, requesting/granted flags, and the protected request after each
   grant. Predict which coders can compile concurrently.
2. Hand-execute heap insertion/removal with EDF keys (deadline, sequence, ID).
   Explain why replacing a removed element may require moving up or down.
3. Derive the overflow guard from `10*value+digit <= INT_MAX`, then demonstrate
   empty text, `0`, `+1`, `1x`, `2147483647`, and `2147483648`.
4. Identify where to change EDF equal-deadline ties to ID before sequence.
   Explain why changing the comparator affects both queues consistently.
5. Trace a shutdown while one worker compiles, one waits for cooldown, and one
   waits for the print gate. Name the condition that wakes each.
6. Draw an ABBA deadlock if a new function acquires output then state while
   another holds state and requests output. Explain the safe ordering.
7. Move the cooldown timestamp to its synchronized release boundary in a copy
   and reproduce the contention probe. Define the release instant precisely.
8. Design an expired-deadline check at compile start without reversing lock
   order or causing a worker to print its own independent death line.
9. Add an explicit failure flag to the private AWK duration checker. Deliberately
   feed it an early-debug log and verify its exit code is nonzero.
10. Explain which conclusions require a subject clarification or scheduling
    redesign, rather than a one-line local patch.

You understand this project when you can trace one worker and the monitor
through a complete cycle, name the lock for every shared field you touch,
explain why each wait can eventually wake, and distinguish intended guarantees
from the implementation's actual limitations.
