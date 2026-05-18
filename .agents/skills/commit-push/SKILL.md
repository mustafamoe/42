---
name: commit-push
description: Use when the user asks to commit, push, commit and push, or says /commit in a git repository.
---

# Commit Push

When this skill is triggered:

1. Run `git status --short`.
2. If there are no changes, say there is nothing to commit and run `git push`.
3. If there are changes, inspect the diff briefly.
4. Stage only relevant changes.
5. Commit with a concise message.
6. Push to the current branch.
7. Run `git status --short` and report whether the working tree is clean.
