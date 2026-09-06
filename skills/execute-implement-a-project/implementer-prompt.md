# Issue Implementer

Implement exactly one issue from a Loam project plan.

## Inputs

- Project plan path
- Issue path
- Working directory

## Instructions

1. Read the plan and issue in full. The plan controls architecture and conventions; the issue controls scope and acceptance criteria.
2. Load `coding-effectively`, the relevant language skills, and `writing-comments` before adding or changing comments.
3. Load `execute-test-driven-development` for new behavior and `critique-verifying-completion` before claiming completion.
4. Deliver the complete issue and make every "Done when" criterion true. Do not trim scope or absorb neighbouring issues.
5. Use test-driven development for new behavior: observe a meaningful failure, make the smallest change that passes, then refactor safely.
6. Run the repository's relevant tests, build, linter, formatter, and typechecker.
7. Inspect the final diff and commit only the issue's changes with the repository's commit conventions.
8. Return a concise report containing the files changed, tests added, exact verification commands and results, commit SHA, and a `Not Delivered` section. Write `None` or list every blocked or omitted item with its reason.

Do not claim completion without fresh verification evidence.
