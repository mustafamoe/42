#!/bin/sh

set -eu

project_dir=$(CDPATH= cd -- "$(dirname "$0")/../submission" && pwd)
test_dir=$(mktemp -d "${TMPDIR:-/tmp}/codexion-test.XXXXXX")
trap 'rm -rf "$test_dir"' EXIT

make -C "$project_dir" fclean >/dev/null
make -C "$project_dir" >/dev/null

if "$project_dir/codexion" 1 2 3 4 5 6 7 invalid \
    >"$test_dir/out" 2>"$test_dir/err"; then
    echo "invalid scheduler was accepted" >&2
    exit 1
fi
test ! -s "$test_dir/out"
test "$(cat "$test_dir/err")" = "Error"

if "$project_dir/codexion" 999999999999999999999 2 3 4 5 6 7 fifo \
    >"$test_dir/out" 2>"$test_dir/err"; then
    echo "overflowing number was accepted" >&2
    exit 1
fi
test ! -s "$test_dir/out"
test "$(cat "$test_dir/err")" = "Error"

"$project_dir/codexion" 1 50 10 10 10 1 0 fifo >"$test_dir/one"
awk '
    $3 == "has" && $4 == "taken" && $5 == "a" && $6 == "dongle" {
        taken++
    }
    $3 == "burned" && $4 == "out" {
        death++
        if ($1 < 50 || $1 > 60) exit 1
    }
    END {exit !(taken == 1 && death == 1)}
' "$test_dir/one"

for policy in fifo edf; do
    "$project_dir/codexion" 5 800 30 10 10 3 5 "$policy" \
        >"$test_dir/$policy"
    if grep -q 'burned out' "$test_dir/$policy"; then
        echo "$policy unexpectedly burned out" >&2
        exit 1
    fi
    awk '
        $3 == "is" && $4 == "compiling" {compiled[$2]++}
        END {
            for (id = 1; id <= 5; id++)
                if (compiled[id] != 3) exit 1
        }
    ' "$test_dir/$policy"
done

"$project_dir/codexion" 5 450 100 50 50 4 20 edf \
    >"$test_dir/edf-liveness"
test "$(grep -c ' is compiling$' "$test_dir/edf-liveness")" -eq 20
if grep -q 'burned out' "$test_dir/edf-liveness"; then
    echo "feasible EDF schedule burned out" >&2
    exit 1
fi

"$project_dir/codexion" 6 200 100 1 1 1 20 edf \
    >"$test_dir/edf-even-ring"
test "$(grep -c ' is compiling$' "$test_dir/edf-even-ring")" -eq 6
if grep -q 'burned out' "$test_dir/edf-even-ring"; then
    echo "feasible even-ring EDF schedule burned out" >&2
    exit 1
fi

"$project_dir/codexion" 20 10000 2 0 0 2 0 fifo \
    >"$test_dir/compile-duration"
awk '
    $3 == "is" && $4 == "compiling" {started[$2] = $1; compiles++}
    $3 == "is" && $4 == "debugging" && $1 - started[$2] < 2 {exit 1}
    END {exit !(compiles == 40)}
' "$test_dir/compile-duration"

"$project_dir/codexion" 18 5000 15 3 0 3 8 edf \
    >"$test_dir/cooldown"
awk '
    $3 == "is" && $4 == "compiling" {
        left = $2 - 1
        right = $2 + 1
        if (left == 0) left = 18
        if (right == 19) right = 1
        if ((seen[left] && $1 - started[left] < 23) ||
            (seen[right] && $1 - started[right] < 23)) exit 1
        started[$2] = $1
        seen[$2] = 1
        compiles++
    }
    END {exit !(compiles == 54)}
' "$test_dir/cooldown"

"$project_dir/codexion" 200 5 100 1 1 2 0 edf \
    >"$test_dir/monitor-precision"
awk '
    $3 == "burned" && $4 == "out" {
        found++
        if ($1 < 5 || $1 > 15) exit 1
    }
    END {exit !(found == 1)}
' "$test_dir/monitor-precision"

awk '
    !($0 ~ /^[0-9]+ [0-9]+ (has taken a dongle|is compiling|is debugging|is refactoring|burned out)$/) {
        exit 1
    }
' "$test_dir/fifo" "$test_dir/edf" "$test_dir/edf-liveness" \
    "$test_dir/edf-even-ring" "$test_dir/compile-duration" \
    "$test_dir/cooldown" "$test_dir/monitor-precision" "$test_dir/one"

make -C "$project_dir" fclean >/dev/null
echo "Codexion tests passed"
