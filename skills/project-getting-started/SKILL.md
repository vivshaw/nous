---
name: project-getting-started
description: Use when starting a project from an approved design spec and preparing its branch, plan, and execution handoff.
---

# Getting Started on a Project

Move an approved design from spec to an isolated branch and executable plan.

## Select the Spec

If the user did not provide a spec path, list candidates under `.gro/tasks/` and ask them to choose. Never infer which spec they mean.

## Set Up the Branch

Derive the project slug from the spec directory. Ask whether to use the current branch or create a named branch from the repository's default branch. Never create or switch branches silently.

If creating a branch:

1. Identify the default branch and current worktree state.
2. Refuse to overwrite or discard unrelated changes.
3. Create the requested branch from the agreed base.
4. Verify and report the active branch.

## Read Project Guidance

Read `.gro/project-plan-guidance.md` when it exists and pass its absolute path into planning and review. If it does not exist, continue without mentioning it.

## Create the Plan

Load `project-writing-plan`. It investigates the codebase and dependencies, writes `plan.md` and issue files, and validates them with an independent review.

Use the host's task tracker for branch setup, optional guidance, planning, and handoff when available.

## Hand Off

Planning and implementation benefit from separate contexts. Verify the repository root and absolute plan directory, then provide this handoff with the actual path:

```text
Use the execute-implement-a-project skill for /absolute/path/.gro/tasks/YYYY-MM-DD-slug/
```

Recommend starting it in a fresh conversation or compacted context when the host supports that. Do not prescribe a host-specific command. If the user asks to continue immediately, proceed with the same execution skill rather than blocking on the context reset.
