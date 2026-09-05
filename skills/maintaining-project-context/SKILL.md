---
name: maintaining-project-context
description: Use near branch completion when contract, API, architecture, invariant, dependency, or domain changes may require AGENTS.md updates.
---

# Maintaining Project Context

Use `writing-agents-md-files` for context-file structure and writing guidance.

`AGENTS.md` records durable contracts and architectural intent. Update it when code changes what future agents must know; do not update it for internal refactors, tests, or bug fixes that preserve contracts.

## Process

1. Diff the branch or phase against its base commit.
2. Categorize changes as structural, contract, behavioral, dependency, or internal.
3. Find the applicable root and nested `AGENTS.md` files.
4. Read each affected context file and verify its claims against current code.
5. Update contracts, dependencies, invariants, decisions, commands, and paths that changed. Remove stale statements.
6. Create a nested `AGENTS.md` only when a domain has enough distinct contracts to justify one. Put information at the lowest scope where it applies.
7. Check whether the repository intentionally maintains host-specific pointer files such as `CLAUDE.md`; preserve that established convention without making it universal.
8. Inspect the diff and commit context changes separately when the repository's workflow calls for it.

## Update When

- Public API or interface signatures change
- New modules or domain boundaries appear
- Invariants or guarantees change
- Dependencies or ownership boundaries change
- A durable architectural decision is made

## Do Not Update For

- Internal implementation changes
- Tests alone
- Formatting or comments
- Bug fixes that restore the documented contract

Return a concise report naming changed context files, unchanged files checked, and any contract that still needs human confirmation.
