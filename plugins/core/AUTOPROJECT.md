# Autoproject

How the autonomous loop actually works, for when you need to debug one.

Three files do all the work: a `Stop` hook that decides whether the turn is really over, `.gro/run.json` that holds the run's state, and `.gro/run.log` that records why the loop stopped.

## Hook

`continue-autonomous-run.py` runs on every `Stop` event, with a 10-second timeout. On each turn it:

1. **Reads `.gro/run.json`:** If the file is not present, or the run `status` is not `active`, it exits immediately.
2. **Claims the run, if needed:** The first time the hook fires, it stamps its `session_id` into the file. This is so any other sessions in the same checkout will see a foreign id and leave the run alone.
3. **Counts checkboxes in `<plan_dir>/plan.md`:** Determines how much work is left and updates `run.json` accordingly.
4. **Prompts to continue:** If there is any remaining work, prompts the agent to continue and points it back at the project plan and next task. If there is no remaining work, exits and allows the run to end.

### How work is counted

Only `plan.md` is scanned, and only checkboxes at column 0. Document order in `plan.md` is execution order. The first unchecked box is always the next thing to do. If we're out of boxes, we're done!

### Guardrails

| Guardrail | Limit | Why |
| --- | --- | --- |
| Continuation cap | 30 stop hooks | A run that can't finish within 30 stop hooks is probably either stuck on something, or working on something overly ambitious. |
| Stall limit | 2 stop hooks in `stalled` status | The agent is stuck on something, and require human guidance to get unstuck. |
| `stop_hook_active` | — | Claude Code sets this on a stop that happens inside a hook-driven continuation, the hook uses this to prevent infinite loops. |

## `run.json`

`.gro/run.json` is used to track Autoproject session progress. Before work is started, it will be initialized by `core:autoproject` in `pending` status. During execution, `core:execute-implement-a-project-autonomously` sets it to `active` and continually updates it.

```json
{
  "plan_dir": ".gro/tasks/2026-08-09-widgets",
  "status": "active",
  "continuations": 0,
  "last_remaining": null,
  "stalls": 0
}
```

| Field | Meaning |
| --- | --- |
| `plan_dir` | Path to the directory holding the project docs, relative to the repo root. |
| `status` | `pending`, `active`, `completed`, `capped`, `stalled`, or `error`. |
| `session_id` | Added by the hook on first fire, to keep track of which agent session is running it. |
| `continuations` | How many times the hook has prompted the agent to continue so far. (Capped at 30.) |
| `last_remaining` | Count of remaining work items. (Used for stall detection.) |
| `stalls` | Consecutive turns with no progress. |

Everything but `plan_dir` and `status` is the hook's bookkeeping. Initialize as above and leave it alone — editing `continuations` or `stalls` to buy more turns defeats the point of having a cap.

## Run Log

`.gro/run.log` contains a line for every decision the stop hook made. Interpret it like so:

| Log says                             | Meaning                                                                                          |
| ------------------------------------ | ------------------------------------------------------------------------------------------------ |
| `completed`                          | The agent completed the entire project.                                                          |
| `halted (capped)`                    | The agent hit the stop hook 30 times and still has work left.                                    |
| `halted (stalled)`                   | The agent has hit the stop hook twice without completing any further work. Something is stalled. |
| `halted (error)`                     | Something is wrong with the plan, such as missing or malformatted plan docs.                     |
| `found an active run claimed by ...` | The session was orphaned. (Delete `session_id` from `.gro/run.json` to re-arm.)                  |

If the file is empty, the hook never ran!
