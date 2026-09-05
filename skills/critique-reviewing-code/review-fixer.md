# Review Fixer

Address a review's complete issue list in a fresh implementation subagent.

1. Read every issue and the affected code before editing.
2. Load the relevant coding, debugging, language, testing, and verification skills.
3. Fix root causes in severity order while keeping the diff limited to the review.
4. If a suggested fix is wrong, apply a better fix and explain the disagreement.
5. Run the repository's relevant tests, build, linter, formatter, and typechecker.
6. Inspect and commit the fixes using the repository's commit conventions.
7. Report each issue's root cause, fix, and verification evidence, followed by the commit SHA and any unresolved concern.

Minor findings are part of the issue list. The goal is zero findings on re-review.
