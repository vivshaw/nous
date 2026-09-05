# Long-Running State Patterns

Long-running work crosses context and session boundaries. Conversation history is not durable state; bridge boundaries with small artifacts and verified repository state.

## Context Strategy

- **Write:** Persist decisions and progress that another session must recover.
- **Select:** Load only the state needed for the current task.
- **Compress:** Summarize conclusions, not raw exploration.
- **Isolate:** Delegate bounded work to fresh subagents.

Use host-provided compaction or fresh conversations at logical boundaries. Never depend on a particular command name or context threshold.

## Durable State

Prefer an existing project plan or issue tracker. Record:

- Completed items and verification evidence
- Current item and exact blocker
- Pending items in execution order
- Relevant commits and changed paths
- Commands needed to restore a working baseline

Git history plus a concise progress file is usually enough. Avoid a second status record when the project plan already contains checkboxes.

## Session Initialization

1. Confirm the working directory and active branch.
2. Read applicable `AGENTS.md` files and the durable plan.
3. Inspect recent commits and worktree changes.
4. Run the smallest useful baseline verification.
5. Resume the first incomplete item rather than relying on remembered conversation state.

## Orchestration

Keep the main session focused on requirements, decisions, and routing. Give subagents one bounded task, explicit inputs, permission boundaries, relevant skills, and an output contract. Ask them to return distilled findings rather than raw logs.

Use faster tiers for bounded scans and stronger reasoning tiers for ambiguous planning or adversarial review. Keep actual model identifiers in host configuration, not portable directives.

## Failure Prevention

| Failure | Prevention |
|---|---|
| Context exhaustion | Work one issue at a time and persist progress |
| Premature completion | Require fresh verification before marking done |
| Duplicate work | Resume from one durable progress record |
| Lost decisions | Record architecture and constraints in the plan |
| Unsafe recovery | Inspect branch and worktree before editing |

Explicit state beats implicit understanding. Tests, commits, and a single progress record make recovery possible across any harness.
