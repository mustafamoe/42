# Push_swap notes

Subject v10.1 and both official checker binaries are stored in `resources/`.
The mandatory submission contains `Makefile`, `README.md`, `push_swap.h`, and
the twelve `.c` source files in `submission/`; no bonus checker is included.

The program validates signed 32-bit unique integers, indexes their sorted
values, directly handles small stacks, and uses binary radix sorting for larger
inputs.

Validation completed on 2026-08-30:

- `cc -Wall -Wextra -Werror`, required Makefile targets, and no relinking.
- Norminette 3.3.60 and authorized-function audit passed.
- Every permutation of sizes 1 through 6 sorted correctly.
- Random sizes 10, 100, and 500 sorted correctly; maxima were 42, 620, and
  5256 operations respectively.
- Duplicate, overflow, sign-only, empty, and malformed inputs were rejected.
- The current subject-required README was added.

The supplied checker executables target other platforms, so operation semantics
were also verified with a private checker outside `submission/`.

