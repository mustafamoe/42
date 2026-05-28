# Agent Instructions

- Keep a single workspace-level `README.md` at the repository root.
- Do not create or update `README.md` files inside individual project directories.
- After finishing a project, write or update a concise `NOTES.md` in that project.
- Use `NOTES.md` for the project idea, key concepts, exercise summaries, commands,
  gotchas, and any essential information needed later for review or defense.
- Keep the root `README.md` as simple as possible.
- Do not add explanations or descriptions to the root `README.md`.
- Use Python 3.10 for Python projects and checks.
- Before considering Python work finished, run `flake8` and `mypy`
  successfully with Python 3.10.
- When the user says `/commit`, `commit`, or `commit and push`, check
  `git status`, stage relevant changes, commit with a concise message, push to
  the current branch, and confirm the working tree is clean.
