*This project has been created as part of the 42 curriculum by mal-hall.*

# Push_swap

## Description

Push_swap sorts integers in stack `a` by printing a valid sequence of the
project's stack operations. Small inputs use direct cases; larger inputs are
ranked and sorted with a binary radix pass.

## Instructions

Build and run the program:

```sh
make
./push_swap 3 2 1
./push_swap "3 2 1"
```

The program writes only operations to standard output. Invalid input writes
`Error` to standard error. `make clean`, `make fclean`, and `make re` provide
the required cleanup and rebuild targets.

## Resources and AI usage

The project subject, C manual pages, and the 42 Norm were used as references.
AI was used to help review edge cases, verify operation sequences, and prepare
exhaustive and randomized tests. The sorting implementation and its behavior
were checked directly before submission.
