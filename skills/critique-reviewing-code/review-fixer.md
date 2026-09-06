# Review Fixer

Address a review's complete issue list in a fresh implementation subagent.

1. Read every issue and the affected code before editing.
2. Load the relevant coding, debugging, language, testing, and verification skills. When Loam Code is installed, load `writing-comments` before adding or changing comments.
3. Fix the complete issue list, including Minor findings. Address each root cause across every affected site, not only the reviewer's example.
4. If a suggested fix is wrong, apply a better fix and explain the disagreement with evidence. Never silently skip a finding.
5. Treat blockers as reportable conditions, not permission to drop the remaining findings.
6. Run the repository's relevant tests, build, linter, formatter, and typechecker.
7. Inspect and commit the fixes using the repository's commit conventions.
8. Report each issue's root cause, fix, and verification evidence, followed by the commit SHA and a `Not Fixed` section listing every disputed or blocked finding.

Minor findings are part of the issue list. The goal is zero findings on re-review.
