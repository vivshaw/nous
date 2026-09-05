---
name: execute-finishing-a-development-branch
description: Use when implementation is complete, all tests pass, and you need to decide how to integrate the work - guides completion of development work by presenting structured options for merge, PR, or cleanup
---

# Finishing a Development Branch

## Overview

Guide completion of development work by presenting clear options and handling chosen workflow.

**Core principle:** Verify tests → detect the working tree → present options → execute → clean up what you created.

**Announce at start:** "I'm using the `execute-finishing-a-development-branch` skill to complete this work."

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
git remote
```

`GIT_DIR` differing from `GIT_COMMON` means you're in a linked worktree, unless the third command returns a path, which means you're in a submodule. A submodule is a normal checkout for these purposes.

| State | Menu | Cleanup |
|---|---|---|
| Normal checkout, on a branch | Named-branch menu (Step 4) | Nothing to remove |
| Normal checkout, detached HEAD | Reduced menu (Step 4) | Nothing to remove |
| Worktree, on a branch | Named-branch menu (Step 4) | By provenance (Step 6) |
| Worktree, detached HEAD | Reduced menu (Step 4) | By provenance (Step 6) |

Record the worktree path now, while you're still in it. Step 6 needs it after you've moved.

Record whether a remote and pull-request capability are available. Do not offer a push-and-PR option in a local-only repository or when no PR capability is available.

### Step 3: Determine Base Branch

```bash
# Try common base branches
git merge-base HEAD main 2>/dev/null || git merge-base HEAD master 2>/dev/null
```

Or ask: "This branch split from main - is that correct?"

### Step 4: Present Options

**A named branch with a usable PR remote: present these 4:**

```
Implementation complete. What would you like to do?

1. Merge back to <base-branch> locally
2. Push and create a Pull Request
3. Keep the branch as-is (I'll handle it later)
4. Discard this work

Which option?
```

**A named branch without a usable PR remote: present these 3:**

```
Implementation complete. What would you like to do?

1. Merge back to <base-branch> locally
2. Keep the branch as-is (I'll handle it later)
3. Discard this work

Which option?
```

**Detached HEAD with a usable PR remote: present these 3:**

```
Implementation complete. This working tree is on a detached HEAD, so there's no branch to merge from yet.

1. Push as a new branch and create a Pull Request
2. Keep as-is (I'll handle it later)
3. Discard this work

Which option?
```

**Detached HEAD without a usable PR remote: present these 2:**

```
Implementation complete. This working tree is on a detached HEAD, so there's no branch to merge from yet.

1. Keep as-is (I'll handle it later)
2. Discard this work

Which option?
```

**Don't add explanation** - keep options concise.

### Step 5: Execute Choice

The option numbers below are for a named branch with a usable PR remote. Map reduced menus explicitly:

- **Named branch without PR:** Option 1 stays Option 1; Option 2 maps to Option 3; Option 3 maps to Option 4.
- **Detached HEAD with PR:** Option 1 asks for a branch name, runs `git switch -c <branch-name>`, then follows Option 2; Option 2 maps to Option 3; Option 3 maps to Option 4.
- **Detached HEAD without PR:** Option 1 maps to Option 3; Option 2 maps to Option 4. There is no branch to delete after worktree cleanup.

#### Option 1: Merge Locally

```bash
# The first worktree entry is this repository's primary checkout, even in a submodule.
PRIMARY_ENTRY=$(git worktree list --porcelain | awk '/^worktree / { sub(/^worktree /, ""); print; exit }')
PRIMARY_ROOT=$(git -C "$PRIMARY_ENTRY" rev-parse --show-toplevel)
cd "$PRIMARY_ROOT"

# Merge first — verify success before removing anything
git checkout <base-branch>

# If the base branch has an upstream, update by fast-forward only.
if UPSTREAM=$(git rev-parse --abbrev-ref --symbolic-full-name '@{upstream}' 2>/dev/null); then
  REMOTE=${UPSTREAM%%/*}
  git fetch "$REMOTE"
  git merge --ff-only "$UPSTREAM"
fi

git merge <feature-branch>

# Verify tests on merged result
<test command>
```

Then proceed to step 6.

#### Option 2: Push and Create PR

```bash
# Push branch
git push -u <remote> <feature-branch>

# Create PR; GitHub example
gh pr create --title "<title>" --body "$(cat <<'EOF'
## Summary
<2-3 bullets of what changed>

## Test Plan
- [ ] <verification steps>
EOF
)"
```

Use the repository host's native PR capability when it is not GitHub.

**Leave the branch in place** — the user needs it alive to iterate on PR feedback.

#### Option 3: Keep As-Is

Report the named branch, or the detached commit SHA and worktree path.

**Don't cleanup branch.**

#### Option 4: Discard

**Confirm first:**
```
This will permanently delete:
- <named branch and its commits, or the detached worktree state>

Type 'discard' to confirm.
```

Wait for exact confirmation.

If confirmed:

```bash
PRIMARY_ENTRY=$(git worktree list --porcelain | awk '/^worktree / { sub(/^worktree /, ""); print; exit }')
PRIMARY_ROOT=$(git -C "$PRIMARY_ENTRY" rev-parse --show-toplevel)
cd "$PRIMARY_ROOT"
# Normal checkout only. A linked worktree must not change another checkout.
git checkout <base-branch>
```

Then proceed to step 6.

### Step 6: Worktree cleanup

**Canonical Options 1 and 4 only.** Option 2 leaves the worktree alone, as your user needs it to iterate on PR feedback. Option 3 keeps everything by definition.

**Worktrees only:** A normal checkout has nothing to release.

**Gro-managed worktrees only:**

- **A host-managed path** belongs to the host. Use its native worktree-exit capability. Don't reach for `git worktree remove`; you would be deleting state the host is still tracking.
- **`.worktrees/` or `worktrees/`** is Gro's own, from the git fallback in `execute-setting-up-a-working-tree`.

**If all 3 conditions above are true**, remove the worktree:

```bash
PRIMARY_ENTRY=$(git worktree list --porcelain | awk '/^worktree / { sub(/^worktree /, ""); print; exit }')
PRIMARY_ROOT=$(git -C "$PRIMARY_ENTRY" rev-parse --show-toplevel)
cd "$PRIMARY_ROOT"
git worktree remove "<worktree-path>"
git worktree prune
```

### Step 7: Branch cleanup

**Named branches, canonical Options 1 and 4 only.** Remove the worktree first because Git cannot delete a branch checked out in another worktree.

```bash
# Option 1, after a successful merge and merged-result tests
git branch -d <feature-branch>

# Option 4, after typed confirmation
git branch -D <feature-branch>
```

Detached HEAD has no branch to delete. Named-branch Options 2 and 3 keep the branch by definition.

## Quick Reference

| Option | Merge | Push | Cleanup Branch | Release Working Tree |
|--------|-------|------|----------------|-------------------|
| 1. Merge locally | yes | - | yes | yes |
| 2. Create PR | - | yes | - | no — needed for PR iteration |
| 3. Keep as-is | - | - | - | no |
| 4. Discard | - | - | yes (force) | yes |

| Worktree path | Who removes it |
|---|---|
| Host-managed path | The host, via its native exit capability. Report and leave if that no-ops |
| `.worktrees/`, `worktrees/` | Gro, via `git worktree remove` from the main repo root |
| No worktree | Nothing to do |

## Common Mistakes

**Skipping test verification**
- **Problem:** Merge broken code, create failing PR
- **Fix:** Always verify tests before offering options

**Open-ended questions**
- **Problem:** "What should I do next?" is ambiguous
- **Fix:** Present exactly the structured options for the working tree's state.

**Removing a worktree the host owns**
- **Problem:** `git worktree remove` on a host-managed path deletes state the host still tracks
- **Fix:** Check provenance first. Host-managed paths use the native exit capability or stay in place

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
