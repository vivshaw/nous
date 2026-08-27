---
name: execute-finishing-a-development-branch
description: Use when implementation is complete, all tests pass, and you need to decide how to integrate the work - guides completion of development work by presenting structured options for merge, PR, or cleanup
user-invocable: false
---

# Finishing a Development Branch

## Overview

Guide completion of development work by presenting clear options and handling chosen workflow.

**Core principle:** Verify tests → detect the working tree → present options → execute → clean up what you created.

**Announce at start:** "I'm using the `core:execute-finishing-a-development-branch` skill to complete this work."

## The Process

### Step 1: Verify Tests

**Before presenting options, verify tests pass:**

```bash
# Run project's test suite
npm test / cargo test / pytest / go test ./...
```

**If tests fail:**
```
Tests failing (<N> failures). Must fix before completing:

[Show failures]

Cannot proceed with merge/PR until tests pass.
```

Stop. Don't proceed to Step 2.

**If tests pass:** Continue to Step 2.

### Step 2: Detect the Working Tree

What type of working tree you're in changes what cleanup is required.

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" && pwd -P)
git rev-parse --show-superproject-working-tree 2>/dev/null
BRANCH=$(git branch --show-current)
```

`GIT_DIR` differing from `GIT_COMMON` means you're in a linked worktree, unless the third command returns a path, which means you're in a submodule. A submodule is a normal checkout for these purposes.

| State | Menu | Cleanup |
|---|---|---|
| Normal checkout | All 4 options | Nothing to remove |
| Worktree, on a branch | All 4 options | By provenance (Step 6) |
| Worktree, detached HEAD | Reduced menu (Step 4) | By provenance (Step 6) |

Record the worktree path now, while you're still in it. Step 6 needs it after you've moved.

### Step 3: Determine Base Branch

```bash
# Try common base branches
git merge-base HEAD main 2>/dev/null || git merge-base HEAD master 2>/dev/null
```

Or ask: "This branch split from main - is that correct?"

### Step 4: Present Options

**Normal checkout, or a worktree on a named branch: present these 4:**

```
Implementation complete. What would you like to do?

1. Merge back to <base-branch> locally
2. Push and create a Pull Request
3. Keep the branch as-is (I'll handle it later)
4. Discard this work

Which option?
```

**Detached HEAD: present these 3:**

```
Implementation complete. This working tree is on a detached HEAD, so there's no branch to merge from yet.

1. Push as a new branch and create a Pull Request
2. Keep as-is (I'll handle it later)
3. Discard this work

Which option?
```

**Don't add explanation** - keep options concise.

### Step 5: Execute Choice

#### Option 1: Merge Locally

```bash
# Get main repo root for CWD safety
MAIN_ROOT=$(git -C "$(git rev-parse --git-common-dir)/.." rev-parse --show-toplevel)
cd "$MAIN_ROOT"

# Merge first — verify success before removing anything
git checkout <base-branch>
git pull
git merge <feature-branch>

# Verify tests on merged result
<test command>
```

Then proceed to step 6.

#### Option 2: Push and Create PR

```bash
# Push branch
git push -u origin <feature-branch>

# Create PR
gh pr create --title "<title>" --body "$(cat <<'EOF'
## Summary
<2-3 bullets of what changed>

## Test Plan
- [ ] <verification steps>
EOF
)"
```

**Leave the branch in place** — the user needs it alive to iterate on PR feedback.

#### Option 3: Keep As-Is

Report: "Keeping branch <name>."

**Don't cleanup branch.**

#### Option 4: Discard

**Confirm first:**
```
This will permanently delete:
- Branch <name>
- All commits: <commit-list>

Type 'discard' to confirm.
```

Wait for exact confirmation.

If confirmed:

```bash
MAIN_ROOT=$(git -C "$(git rev-parse --git-common-dir)/.." rev-parse --show-toplevel)
cd "$MAIN_ROOT"
```

Then proceed to step 6.

### Step 6: Worktree cleanup

**Options 1 and 4 only.** Option 2 leaves the worktree alone, as your user needs it to iterate on PR feedback. Option 3 keeps everything by definition.

**Worktrees only:** A normal checkout has nothing to release.

**Gro-managed worktrees only:**

- **A harness path**, such as `.claude/worktrees/`, `~/.codex/worktrees/`, belongs to the harness. If you have a native exit tool (`ExitWorktree` or similar), use it. Don't reach for `git worktree remove` on a harness path. You would be deleting state the harness is still tracking.
**`.worktrees/` or `worktrees/`** is Gro's own, from the git fallback in `core:execute-setting-up-a-working-tree`.

**If all 3 conditions above are true**, remove the worktree:

```bash
MAIN_ROOT=$(git -C "$(git rev-parse --git-common-dir)/.." rev-parse --show-toplevel)
cd "$MAIN_ROOT"
git worktree remove "<worktree-path>"
git worktree prune
```

## Quick Reference

| Option | Merge | Push | Cleanup Branch | Release Working Tree |
|--------|-------|------|----------------|-------------------|
| 1. Merge locally | yes | - | yes | yes |
| 2. Create PR | - | yes | - | no — needed for PR iteration |
| 3. Keep as-is | - | - | - | no |
| 4. Discard | - | - | yes (force) | yes |

| Worktree path | Who removes it |
|---|---|
| `.claude/worktrees/`, other harness paths | The harness, via its own exit tool. Report and leave if that no-ops |
| `.worktrees/`, `worktrees/` | Gro, via `git worktree remove` from the main repo root |
| No worktree | Nothing to do |

## Common Mistakes

**Skipping test verification**
- **Problem:** Merge broken code, create failing PR
- **Fix:** Always verify tests before offering options

**Open-ended questions**
- **Problem:** "What should I do next?" is ambiguous
- **Fix:** Present exactly the structured options for the working tree's state.

**Removing a worktree the harness owns**
- **Problem:** `git worktree remove` on `.claude/worktrees/` deletes state the harness still tracks
- **Fix:** Check the path first. Harness paths get the native exit tool, or get left alone

**No confirmation for discard**
- **Problem:** Accidentally delete work
- **Fix:** Require typed "discard" confirmation

## Red Flags

**Never:**
- Proceed with failing tests
- Merge without verifying tests on result
- Delete work without confirmation
- Force-push without explicit request
- Run `git worktree remove` on a path the harness created
- Remove a worktree before the merge that depends on it has succeeded

**Always:**
- Verify tests before offering options
- Detect the working tree before presenting options
- Present exactly the options the working tree's state allows
- Get typed confirmation for the discard option
