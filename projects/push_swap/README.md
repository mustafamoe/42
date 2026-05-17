*This project has been created as part of the 42 curriculum by mal-hall.*

# push_swap

## Description

`push_swap` sorts a list of unique integers using two stacks and a limited set of
operations. The program prints the operations needed to sort stack `a` in ascending
order, with the smallest value at the top.

The implementation parses signed integers, rejects duplicates and values outside the
`int` range, indexes the values, and uses small-stack handling for up to five numbers
plus a chunk strategy for larger inputs.

## Instructions

Compile the project:

```sh
make
```

Run it with a list of integers:

```sh
./push_swap 2 1 3 6 5 8
```

Validate the generated instructions with the official checker when available:

```sh
ARG="4 67 3 87 23"
./push_swap $ARG | ./checker_OS $ARG
```

Clean generated files:

```sh
make fclean
```

## Resources

- 42 push_swap subject
- 42 Norm
- Peer testing and checker-based validation

AI was used to help review the subject requirements, run benchmark-style tests,
identify Norm issues, and reorganize files without changing the sorting behavior.
