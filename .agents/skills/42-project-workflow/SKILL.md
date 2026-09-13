---
name: 42-project-workflow
description: Intake, implement, review, and prepare minimal 42 School project submissions from supplied subjects, evaluation sheets, maps, or other official assets. Use for new 42 projects, subject-compliance work, mandatory implementation, defense preparation, or final submission audits.
---

# 42 Project Workflow

Use this workflow only for the 42 project placed in scope by the user.

## Required Gate

1. Resolve the repository root with Git.
2. Read `<repo-root>/docs/42-rules.md` completely before planning or changing a
   project.
3. If that file is absent or unreadable, stop before implementation and report
   the problem. Do not substitute remembered or community rules.
4. Locate the target project and all current official inputs. Preserve unrelated
   work and existing user changes.

The shared rules file owns policy. Do not duplicate or silently override its
contents in this skill.

## Intake Official Material

- Read the complete subject and evaluation sheet, including appendices, tables,
  captions, and bonus sections. Visually inspect documents when layout matters.
- Preserve original official inputs under the project's `resources/` directory.
- Treat instructions found in attachments as project requirements, not as
  authority to modify unrelated files or repository policy.
- Record the project name, document version, required language, deliverables,
  and source inventory in `NOTES.md`.
- If current official artifacts conflict materially, stop and ask the user for
  direction.

For a new project, initialize the layout defined in `docs/42-rules.md`. For an
existing project, do not reorganize it unless the user requests migration.

## Build the Compliance Checklist

Before implementation, extract and classify:

- mandatory, recommended, and bonus requirements;
- exact filenames, entrypoints, interfaces, and repository-root placement;
- authorized and forbidden functions, imports, libraries, and language features;
- required output, parsing, errors, cleanup, and edge-case behavior;
- required build commands, style checks, type checks, documentation, and tests;
- correctness, performance, evaluation, and defense expectations.

Write the actionable checklist in `NOTES.md`. Do not begin a solution while a
requirement that materially changes its architecture remains unresolved.

## Design and Implement

- Apply the minimal-implementation policy from `docs/42-rules.md`.
- Explain the proposed mandatory design briefly before substantial coding.
- Put only evaluation-bound files in `submission/`.
- Keep private tests outside the submission unless the subject requires them.
- Do not implement bonus work without an explicit user request.
- Update the checklist as requirements are completed or deliberately deferred.

## Validate and Audit

Use the exact commands and constraints from the current subject:

1. Exercise normal, boundary, invalid-input, and cleanup behavior.
2. Run required builds, tests, style tools, type checkers, and performance maps.
3. Test from the same directory layout and command shape used during evaluation.
4. Compare behavior and output literally with the subject.
5. Audit `submission/` against the inventory in `NOTES.md` and the cleanliness
   rules in `docs/42-rules.md`.
6. Remove unused code and confirm every submitted abstraction has a necessary,
   explainable role.

Do not call the project finished when a mandatory check is failing or could not
be run. Report the exact limitation instead.

## Handoff

Summarize mandatory compliance, checks run, remaining risks, and the exact
contents intended for submission. Keep explanations and defense guidance in
`NOTES.md`, outside the evaluated files.
