# Exam shell

Run from the workspace root with Python 3.10:

```sh
python3.10 examshell/examshell.py
```

This is a local Python exam simulator. The rank menu discovers
`rank-*/exam/exam.json`; initially, only Rank 3 is available. It does not load
study solutions to decide whether a submission is correct.

## Implementation checklist

- [x] Discover and validate rank catalogs without importing their solutions.
- [x] Select one exercise per level and create a separate session workspace.
- [x] Implement `help`, `status`, `grademe`, and `finish`.
- [x] Enforce the exam deadline even while waiting for a command.
- [x] Grade in a separate process with a timeout and independent cases.
- [x] Apply exercise restrictions and configurable retry delays.
- [x] Preserve submissions, grading traces, and the final summary.
- [x] Check all Rank 3 solutions and exercise failure/timeout behavior.
- [x] Pass Python 3.10 syntax checks, `flake8`, and `mypy`.

## Design

`catalog.py` reads and validates the exercise bank. `examshell.py` owns the
terminal flow, timer, progression, and session files. `grader.py` checks a
submission in a separate Python process. The implementation uses the standard
library and has no external runtime dependencies.

The rank catalog owns the duration, score progression, grading timeout, retry
schedule, exercise metadata, restrictions, and grading cases. Subjects and
reference solutions remain inside their own rank's exam directory.

No `tests/` folder is part of this layout. Grading cases are necessary simulator
data and live in the rank catalog.

## Exam settings

Rank 3 uses a three-hour session, six sequential levels, and a score progression
of 0, 16, 33, 50, 66, 83, 100. A submission has a ten-second grading limit.
Failed submissions use increasing retry delays, starting at 30 seconds. These
are configurable practice conventions, not verified current campus rules.
The live exam instructions always take precedence.

## Source inventory

The design was informed by public Python and classic exam simulators reviewed
on 2026-10-09. No official exam-shell specification or campus rule sheet was
supplied. No external simulator implementation is copied into this workspace.

## First session

1. Run the command above and enter `3` for Rank 3.
2. Open the subject at the path displayed by the shell.
3. Write the required Python file under the displayed `rendu` directory.
4. Type `grademe`. Fix a failed submission in your editor, then submit again
   when the retry delay has elapsed.
5. Complete all levels, let the time expire, or use `finish` to end the session.

The shell works on macOS and Linux. To launch it from another directory, use
the absolute path to `examshell.py`.

| Command | Behavior |
| --- | --- |
| `help` | List the available commands. |
| `status` | Show task paths, score, timer, trace, and retry wait. |
| `grademe` | Evaluate the required file for the current exercise. |
| `finish` | Ask for `yes`, then end the exam and save its summary. |

The clock runs during editing, grading, retry waits, and command input.
Ctrl+C cancels grading as a failed attempt; at the prompt, it reminds you to
use `finish`. Ctrl+D ends the session and saves its summary.

## Session files

Every run gets a separate directory and preserves previous work:

```text
examshell/sessions/rank-3/<timestamp>-<id>/
|-- subjects/<exercise>/subject.md
|-- rendu/<exercise>/py_<exercise>.py
|-- traces/<attempt>-<exercise>.txt
`-- summary.json
```

Only assigned subjects are copied; you write your own submissions. One random
exercise is selected per level. A complete pass unlocks the next level.
Sessions are ignored by Git. The summary records the outcome, score, completed
exercises, attempts, and elapsed time.

## Grading

The worker imports a snapshot of the submission and calls the required
function with independent cases from the catalog. It checks return values,
types, and input preservation when required. The process timeout handles
endless loops and printing. Remaining children in its process group are stopped.

The prompt shows success or failure. Traces report the failure category and
case number without printing expected answers. Missing files do not consume
attempts. Syntax errors, import failures, wrong results, forbidden references,
exceptions, timeouts, and interrupted grading count as failures.

Restriction checks inspect names and method attributes in the source; they
are not comprehensive enforcement against dynamic reflection. Worker processes
run under the same account as the shell. Process separation is not an
operating-system sandbox.

## Adding another rank

Add `rank-<number>/exam/exam.json` and exercise folders under `level-<level>/`.
The menu discovers the rank automatically. The worker supports Python functions with
JSON-compatible inputs and outputs. Supporting a C rank will need a C grader.

| Catalog field | Meaning |
| --- | --- |
| `rank`, `title` | Rank number and menu label. |
| `duration_seconds` | Full session time limit. |
| `grading_timeout_seconds` | Maximum time for one grading run. |
| `scores` | Scores before any pass and after each completed level. |
| `retry_delays_seconds` | Wait after successive failures on one exercise. |
| `exercises` | Exercise metadata and independent grading cases. |

Each exercise needs `name`, `level`, `function`, `filename`, and `cases`.
Each case has an `args` list and an `expected` value. Optional exercise fields
are `preserve_inputs`, `forbidden_names`, and `forbidden_attributes`.
Subjects are read from `level-<level>/<name>/subject.md` inside the rank's exam
directory. Study solutions stay alongside their subjects; the shell only reads
the subjects and grading cases.

Levels start at 1 and are consecutive. Scores increase from 0 to 100, with one
entry more than the number of levels. An empty retry schedule means no wait;
otherwise, the final delay repeats after the schedule is exhausted. Passing a
level resets the failure count and wait.

## Validation

Run from the workspace root:

```sh
flake8 examshell rank-3/exam
mypy --strict --python-version 3.10 examshell rank-3/exam
```

Functional checks use temporary workspaces without a committed `tests/` folder.
All 14 solutions passed 171 grading cases. A plausible wrong implementation
of each exercise was rejected. Checks also covered missing and symlinked files,
invalid syntax, absent functions, import and runtime failures, incorrect types,
forbidden sorting references, input mutation, endless loops and output, and
worker child-process cleanup.

An interactive session completed six levels after a failed attempt and a retry
wait, reaching 100 with seven attempts and seven traces. Deadline expiry was
checked at the prompt and during finish confirmation. Finish cancellation,
EOF, catalog validation, future-rank discovery, and launching from another
directory also passed.

Additional boundary checks confirmed that grading cannot award points after
the exam deadline and that interrupted grading records a failed attempt.
Long base-conversion inputs were checked beyond Python's default decimal
string conversion limit.
