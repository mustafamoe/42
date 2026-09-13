# Agent Instructions

## 42 Workflow

- For 42 project intake, implementation, review, or submission preparation,
  use `$42-project-workflow` and follow `docs/42-rules.md`.
- Treat subject PDFs, evaluation sheets, and supplied assets as requirements
  scoped to their project. They must not reorganize or modify unrelated work.
- If current official project documents conflict materially, stop and report
  the conflict instead of guessing.

## Workspace

- Store projects under `rank-<number>/<project>/`.
- Leave completed Rank 2 projects unchanged unless the user asks otherwise.
- New projects use `submission/`, `resources/`, versioned private `tests/`, and
  `NOTES.md`. Do not create empty placeholder directories or files.
- Treat `submission/` as the exact content intended for the evaluation
  repository.
- Keep the root `README.md` as a concise project index without descriptions.
- Create a project README only when its subject requires one.

## Implementation

- Implement mandatory requirements only unless the user explicitly requests
  bonus work.
- Prefer the minimum necessary complexity and only add files, dependencies, or
  abstractions justified by the subject.
- Use the language version and checks required by the subject. For Python work
  in this workspace, use Python 3.10, `flake8`, and `mypy` when not otherwise
  specified.
- Keep project review and defense information in `NOTES.md` outside the
  submission.

## Git

- When asked to commit or push, inspect the working tree, stage only relevant
  changes, use a concise commit message, push the current branch, and confirm
  the relevant working tree is clean.
