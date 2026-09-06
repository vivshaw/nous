---
name: execute-implement-a-project
description: Use when executing a Loam project plan milestone by milestone with isolated implementation subagents, requirement verification, and review loops.
---

# Implementing a Project

Execute a plan milestone by milestone. Each implementation subagent receives exactly `plan.md` plus one issue file. The plan supplies shared architecture and conventions; the issue supplies scope and acceptance criteria.

If no validated plan exists, use `project-writing-plan` first. If the user has not identified the plan, list `.loam/projects/` and ask which one to execute.

## Prepare

1. Read `plan.md` in full and resume at the first unchecked item.
2. Use `execute-setting-up-a-working-tree` to choose and prepare the implementation checkout.
3. Re-read `plan.md` from that checkout and record absolute paths to the plan, issue directory, spec, and optional `.loam/project-plan-guidance.md`.
4. Use the host's task tracker, if available, for milestone issue work, milestone verification, and wrap-up. `plan.md` remains the durable source of truth.
5. If `plan.md` has no implementation base, record the current commit there before changing code. Use it for the final full-project review.

## Implement Each Issue

Before starting a milestone's first issue, record the current commit in that milestone's `Base commit` field in `plan.md`. Use that base for the milestone review.

For every unchecked issue in order, delegate to a fresh native implementation or generic subagent. Give it:

- The adjacent `implementer-prompt.md`
- The absolute plan path
- The absolute path to exactly one issue
- The working directory

After the subagent returns, inspect its evidence and relevant diff. Tick the issue checkbox only after its acceptance criteria and verification pass. Do not review between issues; review at the milestone gate.

The issue defines the complete work for that dispatch. Require every acceptance criterion; issue boundaries prevent absorbing neighbouring work, not trimming the assigned scope.

If subagents are unavailable, follow the same prompt directly and keep issue boundaries explicit.

## Verify Each Milestone

1. Run the tests that cover every requirement named by the milestone's `Verifies:` line.
2. Use `critique-reviewing-code` over the milestone's commit range, plan, and issue files.
3. Fix every finding and re-review until zero remain.
4. Stop and ask the user if the same finding survives three cycles.
5. Tick the milestone gate only after requirement tests pass and review is clean.

If review exceeds context limits, split the commit range into logical sections rather than skipping review.

## Wrap Up

Work the plan's wrap-up checkboxes in order:

1. Delegate project-context maintenance to a fresh generic subagent. Give it the base commit, current `HEAD`, working directory, and tell it to load `maintaining-project-context`.
2. Run `critique-reviewing-code` over the full project range. Also verify that every spec requirement belongs to a milestone or the deferred list, and flag deferred P10 requirements.
3. Delegate test analysis using the adjacent `test-analyst-prompt.md`. If it fails, delegate the missing-test work to a fresh implementation subagent with the complete analysis and relevant plan paths, then repeat. Write the passing human test plan beside `plan.md` as `<plan-directory>/test-plan.md`.
4. Summarize each milestone, review cycles, verification evidence, and any compromise or unrun check.
5. Use `execute-finishing-a-development-branch`. Do not merge or deploy without the user's explicit choice.

Never tick unverified boxes. A host task list is temporary; `plan.md` is the resumption contract.
