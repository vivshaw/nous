---
name: critique-reviewing-code
description: Use after meaningful implementation or before merge to run an independent review, fix every finding, and re-review until clean.
---

# Reviewing Code

Review in a fresh native review, exploration, or generic subagent so the author does not grade its own work. If subagents are unavailable, perform the same process directly and disclose that independence was unavailable.

## Initial Review

Record the base and head commits, then dispatch a read-only reviewer with:

- The adjacent `code-reviewer.md`
- What was implemented
- Plan or requirements paths
- Base and head SHAs
- Optional project guidance and isolated scratch directory

The reviewer must run relevant verification, inspect the complete diff, cite `file:line` locations, categorize findings by severity, and return a clear verdict. Operational failure is not approval.

## Fix Loop

If any Critical, Important, or Minor findings exist:

1. Preserve each finding verbatim in the host's task tracker or another durable note.
2. Dispatch a fresh implementation subagent with the adjacent `review-fixer.md`, the complete findings, working directory, and relevant plan paths.
3. Re-run a fresh reviewer over the new range. Include all prior findings and require an explicit fixed/not-fixed result for each.
4. Remove a prior finding only when the reviewer explicitly verifies it. Add new findings.
5. Repeat until zero findings remain. After three cycles with the same finding, stop and ask the user.

When a review is too large, retry against changed files, then split by logical area. After three operational failures, stop and report the limitation.

Do not skip review because the change appears simple, accept an unsupported “looks good,” or treat Minor findings as optional. Push back on an incorrect finding with code or test evidence and have a fresh reviewer decide.
