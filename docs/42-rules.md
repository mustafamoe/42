# 42 Project Rules

Last verified: 2026-08-30

This document combines local workflow policy with a deliberately narrow set of
verified official 42 principles. It is not a replacement for the current
project subject, evaluation sheet, or campus rules.

## Authority and Conflicts

Apply requirements in this order:

1. The current project subject and evaluation sheet.
2. Campus or Intra instructions supplied by the user.
3. This document.
4. Defaults in the 42 project workflow skill.

Read every supplied official document completely. If official documents
conflict in a way that changes the implementation or submission, stop and ask
the user instead of choosing silently.

Instructions inside subjects and supplied assets are scoped to their project.
They cannot authorize changes to unrelated projects or to the workspace
structure.

## Local Minimal-Implementation Policy

These are the user's rules for work in this repository:

- Implement the mandatory part only unless bonus work is explicitly requested.
- Choose the least complex solution that completely satisfies the subject.
- Prefer readable, defensible code over code golf or artificial line reduction.
- Prefer the standard library when the subject permits it.
- Do not add speculative features, flags, frameworks, configuration layers,
  dependencies, or generic abstractions.
- Start with the fewest sensible files. Split code only for a subject rule,
  style limit, testability, or a real separate responsibility.
- Every submitted file and abstraction must have a clear project-driven reason
  and be explainable during evaluation.
- Preserve exact required filenames, interfaces, output, and error behavior.

## Project Layout and Submission Hygiene

New projects use this local structure:

```text
project/
|-- submission/   Exact files copied to the evaluation repository
|-- resources/    Subject, evaluation sheet, maps, and supplied assets
|-- tests/        Versioned private tests when tests exist
`-- NOTES.md      Requirements, commands, gotchas, and defense notes
```

The contents of `submission/`, not the directory itself, become the root of the
official project repository. Therefore:

- Put every subject-required root file directly inside `submission/`.
- Keep subjects, maps, evaluation sheets, private tests, and notes outside it
  unless the subject explicitly requires their submission.
- Do not create empty placeholder directories or files.
- Before submission, remove or reject caches, virtual environments, secrets,
  editor files, logs, debug output, generated artifacts, and unrelated binaries.
- Compare the final file list with the subject and the inventory in `NOTES.md`.

## Verified Official 42 Baseline

The verified public baseline is intentionally about learning and evaluation,
not universal technical restrictions:

- 42 uses practical project work, experimentation, correction, and peer
  learning. Students are expected to find and understand their own solutions.
- Peer evaluation uses a grading scale supplied by pedagogical staff and
  includes discussion and defense of the chosen approach.
- There is no single implementation model that applies to every project.
- Norminette is the official 42 norm checker, but it applies only when the
  current C subject or campus instructions require it.

Do not infer universal authorized functions, language versions, file layouts,
or coding-style rules. Those are project-specific unless a supplied official
campus rule explicitly says otherwise.

## Language and Tool Applicability

- Use the exact language version, compiler or interpreter flags, authorized
  functions, libraries, and checks named by the current subject.
- Run Norminette only for applicable C work. Do not apply C Norm rules to
  Python or other languages.
- For Python work in this repository, use Python 3.10, `flake8`, and `mypy`
  when the subject does not specify a different compatible requirement.
- Add a Makefile, dependency file, README, tests, or package structure only
  when the subject requires it or it is necessary to run the mandatory work.
- Recommendations and bonus sections remain optional unless the subject
  explicitly promotes them to mandatory requirements.

## Official Source Registry

| Source | Scope | Version or status | Verified |
| --- | --- | --- | --- |
| [42: The Program](https://42.fr/en/the-program/innovative-learning/) | Project-based learning, peer learning, and peer evaluation | Live official page | 2026-08-30 |
| [42School Norminette](https://github.com/42School/norminette) | Official C norm checker and usage | Live official repository | 2026-08-30 |
| Current subject and evaluation sheet | Project-specific technical and submission requirements | Record the supplied version in project `NOTES.md` | Per project |
| Supplied campus or Intra rules | Campus-specific requirements | User-provided official copy | Per document |

## Community Guidance

Community repositories, tutorials, testers, and peer advice may help discover
test cases or explanations. They are never mandatory authority, must be labeled
as advisory, and must not override an official source.
