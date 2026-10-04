"""Private output and timing checks, run with Python 3.10."""

import re
import subprocess
import sys
import time
from pathlib import Path


LINE = re.compile(
    r"([0-9]+) ([0-9]+) (has taken a dongle|is compiling|"
    r"is debugging|is refactoring|burned out)"
)


def invalid_inputs(program: Path) -> None:
    valid = ["2", "800", "30", "10", "10", "3", "5", "fifo"]
    cases = [[], valid[:-1], valid + ["extra"]]
    for index, value in [
        (0, "0"), (0, "2147483648"), (0, "999999999999999999999"),
        (1, "0"), (5, "0"), (7, "invalid"), (7, "EDF"),
    ]:
        case = valid.copy()
        case[index] = value
        cases.append(case)
    for index in range(7):
        for value in ["", "-1", "+1", " 1", "1.5", "1x"]:
            case = valid.copy()
            case[index] = value
            cases.append(case)
    for case in cases:
        result = subprocess.run(
            [str(program), *case], capture_output=True, text=True, timeout=5
        )
        assert result.returncode != 0, f"Accepted invalid input: {case}"
        assert result.stdout == "" and result.stderr == "Error\n", case


def check_run(program: Path, arguments: str, expect_death: bool) -> None:
    args = arguments.split()
    count, burnout, compile_ms, debug, refactor, goal, cooldown = map(
        int, args[:7]
    )
    started = time.monotonic()
    result = subprocess.run(
        [str(program), *args], capture_output=True, text=True, timeout=15
    )
    elapsed = (time.monotonic() - started) * 1000
    assert result.returncode == 0 and not result.stderr, result.stderr
    last_compile = [0] * count
    starts: list[list[int]] = [[] for _ in range(count)]
    phase: list[tuple[str, int]] = [("start", 0)] * count
    available = [0] * count
    takes = [0] * count
    previous_time = 0
    dead = False
    for line in result.stdout.splitlines():
        match = LINE.fullmatch(line)
        assert match is not None, f"Invalid log: {line!r}"
        timestamp, coder_id = int(match[1]), int(match[2])
        event = match[3]
        index = coder_id - 1
        assert 0 <= index < count and timestamp >= previous_time, line
        assert not dead, f"Output after burnout: {line}"
        previous_time = timestamp
        if event == "burned out":
            deadline = last_compile[index] + burnout
            assert deadline <= timestamp <= deadline + 10, (arguments, line)
            dead = True
        elif event == "has taken a dongle":
            takes[index] += 1
        elif event == "is compiling":
            assert count > 1 and takes[index] == 2, line
            assert timestamp < last_compile[index] + burnout, line
            assert phase[index][0] in ("start", "is refactoring"), line
            if phase[index][0] == "is refactoring":
                assert timestamp - phase[index][1] >= refactor, line
            for dongle in (index, (index + 1) % count):
                assert timestamp >= available[dongle], (arguments, line)
                available[dongle] = timestamp + compile_ms + cooldown
            last_compile[index] = timestamp
            starts[index].append(timestamp)
            takes[index] = 0
            phase[index] = (event, timestamp)
        elif event == "is debugging":
            assert phase[index][0] == "is compiling", line
            assert timestamp - last_compile[index] >= compile_ms, line
            phase[index] = (event, timestamp)
        else:
            assert phase[index][0] == "is debugging", line
            assert timestamp - phase[index][1] >= debug, line
            phase[index] = (event, timestamp)
    assert dead == expect_death, (arguments, result.stdout)
    if count == 1:
        assert takes == [1] and starts == [[]], result.stdout
    if not dead:
        assert all(len(times) >= goal for times in starts), arguments
        assert all(elapsed >= times[goal - 1] + compile_ms for times in starts)


def main() -> None:
    program = Path(sys.argv[1]).resolve()
    if len(sys.argv) == 3:
        subprocess.run([sys.argv[2]], check=True, timeout=10)
    invalid_inputs(program)
    for policy in ("fifo", "edf"):
        for arguments, death in [
            ("1 50 10 10 10 1 0", True),
            ("2 800 20 10 10 3 5", False),
            ("5 800 30 10 10 3 5", False),
            ("4 1000 0 0 0 10 0", False),
            ("4 30 80 0 0 1 0", True),
            ("4 100 10 200 0 2 0", True),
            ("4 100 10 0 200 2 0", True),
            ("2 100 10 0 0 2 200", True),
        ]:
            check_run(program, f"{arguments} {policy}", death)
    for arguments, death in [
        ("5 450 100 50 50 4 20 edf", False),
        ("5 340 100 0 0 3 20 edf", False),
        ("6 260 100 1 1 1 20 edf", False),
        # All have started once, but not all have finished before burnout.
        ("6 200 100 1 1 1 20 edf", True),
        ("20 10000 2 0 0 2 0 fifo", False),
        ("18 5000 15 3 0 3 8 edf", False),
        ("200 5 100 1 1 2 0 edf", True),
    ]:
        check_run(program, arguments, death)
    print("Codexion integration checks passed")


if __name__ == "__main__":
    main()
