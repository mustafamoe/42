# push_swap

## Idea

Sort unique integers using two stacks and the allowed push_swap operations.

## Key Concepts

- Validate signed integers, duplicates, and `int` range limits.
- Assign sorted indexes to values before sorting.
- Use dedicated small-stack logic for up to five values.
- Use chunk-based moves for larger inputs.

## Commands

```sh
make
./push_swap 2 1 3 6 5 8
make fclean
```

With the official checker:

```sh
ARG="4 67 3 87 23"
./push_swap $ARG | ./checker_OS $ARG
```

## Gotchas

- Input must contain unique integers only.
- Error handling must reject overflow and malformed arguments.
- The program prints operations only; validation is done with a checker.
