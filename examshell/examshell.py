"""Interactive exam sessions for the rank catalogs in this workspace."""

import json
import math
import os
import random
import select
import shutil
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

from catalog import Exercise, Rank, load_rank
from grader import Grade, grade


ROOT = Path(__file__).resolve().parents[1]
SESSIONS = Path(__file__).resolve().parent / "sessions"


def read_line(prompt: str, deadline: float | None = None) -> str:
    """Wait for a line without letting the exam run beyond its deadline."""
    print(prompt, end="", flush=True)
    buffer = bytearray()
    while True:
        remaining = None if deadline is None else deadline - time.monotonic()
        if remaining is not None and remaining <= 0:
            raise TimeoutError
        ready, _, _ = select.select([sys.stdin], [], [], remaining)
        if not ready:
            raise TimeoutError
        # Avoid buffered readline prefetching commands past select's view.
        char = os.read(sys.stdin.fileno(), 1)
        if not char:
            raise EOFError
        if char == b"\n":
            return buffer.decode("utf-8", errors="replace").strip().lower()
        buffer.extend(char)


def clock(seconds: float) -> str:
    total = max(0, math.ceil(seconds))
    hours, rest = divmod(total, 3600)
    minutes, seconds_left = divmod(rest, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds_left:02d}"


def choose_rank() -> Rank | None:
    ranks: dict[int, Rank] = {}
    for manifest in sorted(ROOT.glob("rank-*/exam/exam.json")):
        try:
            rank = load_rank(manifest)
        except (OSError, UnicodeError, ValueError) as error:
            print(f"Cannot load {manifest.relative_to(ROOT)}: {error}")
            continue
        ranks[rank.number] = rank
    if not ranks:
        print("No valid rank catalogs are available.")
        return None

    print("\nExam shell — local Python practice\n")
    for number, rank in sorted(ranks.items()):
        print(f"  {number}. {rank.title} ({len(rank.levels)} levels)")
    print("  q. Quit\n")
    while True:
        try:
            answer = read_line("Choose rank: ")
        except (EOFError, KeyboardInterrupt):
            print()
            return None
        if answer == "q":
            return None
        if answer.isdecimal() and int(answer) in ranks:
            return ranks[int(answer)]
        print("Enter one of the listed rank numbers, or q.")


class Session:
    """Own the timer, assignments, attempts, and files of a single exam."""

    def __init__(self, rank: Rank, sessions: Path = SESSIONS) -> None:
        self.rank = rank
        self.started_at = datetime.now(timezone.utc)
        name = self.started_at.strftime("%Y%m%dT%H%M%SZ")
        self.root = sessions / f"rank-{rank.number}" / (
            f"{name}-{uuid.uuid4().hex[:6]}"
        )
        self.root.mkdir(parents=True)
        self.assignments = [
            random.choice([
                exercise for exercise in rank.exercises
                if exercise.level == level
            ])
            for level in rank.levels
        ]
        self.started = time.monotonic()
        self.deadline = self.started + rank.duration_seconds
        self.completed = 0
        self.attempts = 0
        self.failures = 0
        self.retry_at = self.started
        self.last_trace: Path | None = None

    @property
    def remaining(self) -> float:
        return max(0.0, self.deadline - time.monotonic())

    @property
    def exercise(self) -> Exercise:
        return self.assignments[self.completed]

    @property
    def submission(self) -> Path:
        return (
            self.root / "rendu" / self.exercise.name / self.exercise.filename
        )

    def assign(self) -> None:
        exercise = self.exercise
        subject = self.root / "subjects" / exercise.name / "subject.md"
        subject.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(exercise.subject, subject)
        self.submission.parent.mkdir(parents=True, exist_ok=True)
        self.failures = 0
        self.retry_at = time.monotonic()
        self.last_trace = None
        self.status()

    def status(self) -> None:
        exercise = self.exercise
        print(f"\n{self.rank.title} | Level {exercise.level}/"
              f"{len(self.assignments)} | Score "
              f"{self.rank.scores[self.completed]}/100")
        print(f"Time left: {clock(self.remaining)}")
        print(f"Exercise: {exercise.name}")
        subject = self.root / "subjects" / exercise.name / "subject.md"
        print(f"Subject:  {subject}")
        print(f"Submit:   {self.submission}")
        delay = self.retry_at - time.monotonic()
        if delay > 0:
            print(f"Next grading request in: {clock(delay)}")
        if self.last_trace is not None:
            print(f"Trace:    {self.last_trace}")
        print()

    def submit(self) -> None:
        delay = self.retry_at - time.monotonic()
        if delay > 0:
            print(f"Wait {clock(delay)} before another grading request.")
            return
        if not self.submission.is_file():
            print(f"Create the required file first: {self.submission}")
            return
        exercise = self.exercise
        self.attempts += 1
        print("Grading...", flush=True)
        try:
            verdict = grade(
                self.submission,
                exercise.function,
                exercise.cases,
                min(self.rank.grading_timeout_seconds, self.remaining),
                exercise.preserve_inputs,
                exercise.forbidden_names,
                exercise.forbidden_attributes,
            )
        except KeyboardInterrupt:
            print()
            verdict = Grade(False, "Grading was interrupted.")
        # Finishing after the deadline cannot earn points.
        passed = verdict.passed and self.remaining > 0
        message = verdict.message if self.remaining > 0 else "Time expired."
        traces = self.root / "traces"
        traces.mkdir(exist_ok=True)
        self.last_trace = traces / f"{self.attempts:03d}-{exercise.name}.txt"
        label = "SUCCESS" if passed else "FAILURE"
        self.last_trace.write_text(
            f"Exercise: {exercise.name}\nAttempt: {self.attempts}\n"
            f"Verdict: {label}\n{message}\n",
            encoding="utf-8",
        )
        print(f">>>>>>>>>> {label} <<<<<<<<<<")
        print(f"Trace: {self.last_trace}")
        if passed:
            self.completed += 1
            if self.completed < len(self.assignments):
                self.assign()
        else:
            self.failures += 1
            schedule = self.rank.retry_delays_seconds
            if schedule:
                delay = schedule[min(self.failures - 1, len(schedule) - 1)]
                self.retry_at = time.monotonic() + delay
                print(f"Next grading request in: {clock(delay)}")

    def finish(self, outcome: str) -> None:
        score = self.rank.scores[self.completed]
        summary = {
            "rank": self.rank.number,
            "started_at": self.started_at.isoformat(),
            "finished_at": datetime.now(timezone.utc).isoformat(),
            "outcome": outcome,
            "score": score,
            "completed": [
                exercise.name for exercise in self.assignments[:self.completed]
            ],
            "attempts": self.attempts,
            "elapsed_seconds": round(time.monotonic() - self.started, 2),
        }
        (self.root / "summary.json").write_text(
            json.dumps(summary, indent=2) + "\n", encoding="utf-8",
        )
        progress = f"{self.completed}/{len(self.assignments)} levels"
        print(f"\n{outcome} — {progress}, {score}/100.")
        print(f"Session saved: {self.root}")

    def run(self) -> None:
        print(f"\nSession: {self.root}")
        print("Edit your submission in a second terminal or your editor.")
        print("Commands: help, status, grademe, finish.")
        outcome = "Finished"
        try:
            self.assign()
            while self.completed < len(self.assignments) and self.remaining:
                try:
                    command = read_line("examshell> ", self.deadline)
                    if command == "help":
                        print("help     Show these commands\n"
                              "status   Show task, paths, score, and timer\n"
                              "grademe  Grade the required submission file\n"
                              "finish   End this exam and save its summary")
                    elif command == "status":
                        self.status()
                    elif command == "grademe":
                        self.submit()
                    elif command == "finish":
                        answer = read_line("End this exam? Type yes: ",
                                           self.deadline)
                        if answer == "yes":
                            break
                        print("Continuing the exam.")
                    elif command:
                        print("Unknown command. Type help for commands.")
                except KeyboardInterrupt:
                    print("\nUse finish to end the exam. Timer still running.")
            if self.completed == len(self.assignments):
                outcome = "Passed"
            elif not self.remaining:
                outcome = "Time expired"
        except TimeoutError:
            print()
            outcome = "Time expired"
        except EOFError:
            print()
            outcome = "Disconnected"
        except OSError as error:
            print(f"\nSession error: {error}")
            outcome = "Interrupted"
        finally:
            self.finish(outcome)


def main() -> None:
    rank = choose_rank()
    if rank is not None:
        try:
            Session(rank).run()
        except OSError as error:
            print(f"Could not create or save the session: {error}")


if __name__ == "__main__":
    main()
