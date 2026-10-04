#!/bin/sh

set -eu

project_dir=$(CDPATH= cd -- "$(dirname "$0")/../submission" && pwd)
test_dir=$(mktemp -d "${TMPDIR:-/tmp}/codexion-test.XXXXXX")
trap 'rm -rf "$test_dir"; make -C "$project_dir" fclean >/dev/null' EXIT

make -C "$project_dir" fclean >/dev/null
make -C "$project_dir" >/dev/null
make -C "$project_dir" -q

${CC:-cc} -Wall -Wextra -Werror -pthread -I"$project_dir/include" \
    "$project_dir/../tests/regression.c" \
    "$project_dir/src/heap.c" "$project_dir/src/log.c" \
    "$project_dir/src/monitor.c" -o "$test_dir/regression"
${PYTHON:-python3.10} "$project_dir/../tests/test.py" \
    "$project_dir/codexion" "$test_dir/regression"
