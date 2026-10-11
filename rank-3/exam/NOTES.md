# Rank 3 exam practice

Exercises are grouped into `level-1/` through `level-6/`. Inside each level,
each exercise has its own folder containing `subject.md` and a Python solution.
Read the subject first, attempt it independently, then compare your reasoning
with the solution. The brief docstrings and comments explain the code; this
file gives the wider study guidance.

## Implementation checklist

- [x] Organize all 14 existing solutions into exercise folders.
- [x] Group exercise folders by their level in the exam catalog.
- [x] Write a study subject with signature, filename, rules, and examples.
- [x] Correct the permutation spelling and clean up printed demonstrations.
- [x] Explain the algorithms and important edge cases.
- [x] Supply the Rank 3 catalog for the shared exam shell.
- [x] Validate the solutions against independent grading cases.
- [x] Pass Python 3.10 syntax checks, `flake8`, and `mypy`.

## Requirements and source inventory

The inventory contains 14 existing Python practice solutions. Study briefs
describe their exercise contracts; no original official subject PDFs or
evaluation sheets were supplied. Community exercise descriptions reviewed on
2026-10-09 are advisory. For a live exam, follow the subject shown there.

This is a practice collection, not a project submission repository. The shared
shell lives outside the rank directories, and this folder has no `tests/`
directory. The exercise catalog contains the independent grading cases used
by the simulator.

## Exercise index

| Level | Exercise | Main idea |
| --- | --- | --- |
| 1 | [bracket_validator](level-1/bracket_validator/subject.md) | Stack and nested pairs |
| 1 | [cryptic_sorter](level-1/cryptic_sorter/subject.md) | Stable insertion sort |
| 2 | [echo_validator](level-2/echo_validator/subject.md) | Normalization and reversal |
| 2 | [mirror_matrix](level-2/mirror_matrix/subject.md) | Nested lists and slicing |
| 3 | [hidenp](level-3/hidenp/subject.md) | Ordered subsequence |
| 3 | [inter](level-3/inter/subject.md) | Membership and uniqueness |
| 3 | [number_base_converter](level-3/number_base_converter/subject.md) | Digit alphabets and division |
| 3 | [pattern_tracker](level-3/pattern_tracker/subject.md) | Adjacent pairs |
| 4 | [anagram](level-4/anagram/subject.md) | Normalized character counts |
| 4 | [shadow_merge](level-4/shadow_merge/subject.md) | Two-pointer merge |
| 4 | [string_permutation_checker](level-4/string_permutation_checker/subject.md) | Exact character counts |
| 5 | [string_sculptor](level-5/string_sculptor/subject.md) | Letter index and parity |
| 5 | [twist_sequence](level-5/twist_sequence/subject.md) | Modulo and list slices |
| 6 | [whisper_cipher](level-6/whisper_cipher/subject.md) | Alphabet offsets and modulo |

## Using the shared shell

From the workspace root:

```sh
python3.10 examshell/examshell.py
```

Choose Rank 3, read the assigned subject, and write your function at the
submission path shown by the shell. Use a second terminal or your editor.
Run `grademe` in the exam shell to submit. A passing exercise unlocks the
next level. Study solutions are never copied into the session.

The study file is named after the exercise, for example
`level-4/anagram/anagram.py`.
The session requires the filename shown in its subject, for example
`rendu/anagram/py_anagram.py`. That file must define `anagram`.

## Running a study example

From this directory:

```sh
cd level-4/anagram
python3.10 -c 'from anagram import anagram; print(anagram("rail safety", "Fairy tales"))'
```

This prints `True`. Importing a study file by itself produces no output.

## How the solutions work

### bracket_validator

A stack remembers opening brackets. On a closing bracket, remove the most recent opening bracket and compare its type. An empty stack before a closing bracket is a failure, and a nonempty stack at the end means something never closed. For `([)]`, the `)` tries to close `[` and fails immediately.

### cryptic_sorter

Insertion sort builds the result one word at a time. The helper returns a tuple of the three sorting keys; Python compares tuples from left to right. The `<=` comparison moves past words with equal keys, so ties keep their input order. For ASCII words, identical lowercase text also has the same vowel count, but the third key is retained to express the subject's full ordering.

### echo_validator

Collect letters in lowercase, join them into one string, and compare that string with its reversed slice. `bool(cleaned)` makes the empty-letter case false. For `No lemon, no melon!`, normalization produces `nolemonnomelon`, which matches its reverse.

### mirror_matrix

Walk through the rows and append `row[::-1]` to a new outer list. The slice creates a new row, so the original data is preserved. This is a horizontal reflection, not a transpose or a reversal of the row order.

### hidenp

Keep an index for the next character needed from `small`. Scan `big` once and advance that index only on a match. Return as soon as all of `small` has matched; this also avoids indexing beyond its end. A subsequence preserves order, whereas a substring must also be consecutive.

### inter

Scan `s1`, checking whether each character belongs to `s2` and has not already been added. Those two checks enforce intersection and uniqueness while preserving order. A set alone would lose the ordering required by the subject.

### number_base_converter

Validate the bases and digit alphabet, then build the integer one digit at a
time: multiply the current value by the source base and add the next digit.
Repeated division by the target base produces digits from right to left.
Put each remainder's digit at the front of the result. The separate zero
return is needed because the division loop does not run for zero. Building
the integer manually also supports valid decimal strings longer than the
interpreter's default conversion limit.

### pattern_tracker

Visit each position that has a following character. Confirm that both characters are ASCII digits, then compare their numeric values. Moving the index by one allows overlapping pairs. Restricting the loop to `len(text) - 1` keeps the next-character lookup within bounds.

### anagram

First lowercase both strings and remove spaces. Count every remaining character in a dictionary for each string, then compare those dictionaries. Checking lengths first rules out obvious mismatches. This differs from the permutation exercise because it deliberately ignores case and spaces.

### shadow_merge

Track the next unused position in each list. Compare those values and append the smaller one, advancing only that list's index. When one list runs out, append the other list's remaining slice. Since the inputs are already sorted, there is no need to sort the result.

### string_permutation_checker

Count the characters of both strings without normalizing them. Matching dictionaries mean that every character occurs equally often. A set comparison is insufficient because sets discard repeated occurrences. Unlike `anagram`, this exercise preserves case and all whitespace.

### string_sculptor

Use a counter for letters rather than for every character. Even counters produce lowercase and odd counters produce uppercase. Reset the counter on a space. Digits and punctuation are copied directly, which is why `ab12cd` becomes `aB12cD`.

### twist_sequence

Reduce `k` modulo the list length to discard complete revolutions. Join the last `k` elements with the preceding elements. Handle the empty list before taking the modulo, because its length is zero. At `k == 0`, the slices are the whole list and an empty list, so the expression still works.

### whisper_cipher

Turn a letter into its zero-based offset from `a` or `A`. Add the shift and take the remainder modulo 26 to wrap around, then convert the result back to a character. Separate uppercase and lowercase branches preserve case. Python's modulo also handles negative shifts correctly.

## Checks

Run these from the workspace root:

```sh
flake8 examshell rank-3/exam
mypy --strict --python-version 3.10 examshell rank-3/exam
```

The catalog contains 171 independent grading cases covering the subjects,
empty inputs, repetitions, stable ordering, invalid bases, spaces and tabs,
rotation boundaries, and cipher wraparound. List-producing exercises also
check that their inputs are preserved.

A no-letter palindrome is false. `anagram` ignores ordinary spaces and case;
`string_permutation_checker` ignores neither. `string_sculptor` counts letters
only, and an ordinary space resets that count. `number_base_converter` rejects
non-ASCII characters before uppercasing, so characters that expand or change
into ASCII letters cannot become valid digits accidentally.
