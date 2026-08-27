---
name: execute-setting-up-a-working-tree
description: Use at the start of implementation, before any code is written - settles whether the work gets its own worktree, a new branch, or the current checkout, then prepares that working tree and verifies a clean baseline
user-invocable: false
---

# Setting Up a Working Tree

## Overview

Decide where implementation is going to happen, and put it there.

**Announce at start:** "I'm using the `core:execute-setting-up-a-working-tree` skill to settle where this implementation runs."

## When to Use

- `core:execute-implement-a-project` or `core:execute-implement-a-project-autonomously` is about to start

**Don't use when:**
- Design or planning is still in progress. Planning writes markdown into `.gro/` and commits nothing — there's nothing yet to isolate, and the plan is carried across at Step 4 if it needs to be

## 1. Detect where you already are

Work out whether you're already in a worktree before asking anything. Creating a second worktree on top of the first could cause the session to end up with orphaned branches nobody can find.

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" && pwd -P)
git rev-parse --show-superproject-working-tree 2>/dev/null
git branch --show-current
```

`GIT_DIR` differing from `GIT_COMMON` means either a linked worktree, or a submodule. The third command settles this: any path in the output means a submodule. A submodule is a normal checkout for these purposes.

| What you find | What to do |
|---|---|
| A worktree, on a branch | Report the path and branch. Skip to Step 5 |
| A worktree, detached HEAD | Report it as externally managed. Skip to Step 5 |
| A submodule, or a normal checkout on a non-default branch | Mention the branch, then proceed to Step 2 |
| A normal checkout on the default branch | Proceed to Step 2 |

Already being isolated is the common case for a resumed run. Detection is what makes resumption safe, so run it even when you're confident.

## 2. Ask how to isolate the work

```
Question: "Where should this implementation run?"
Options:
  - "Its own worktree" (a separate checkout, so this one stays yours to use)
  - "A new branch here" (e.g. [slug], or $(whoami)/[slug])
  - "This branch" (no isolation)
```

Take the slug from the plan directory name — everything after `YYYY-MM-DD-`.

## 3. Carry out the choice

### 3a. Its own worktree

**First, check what you'd be branching from.** Native worktree tools commonly branch from `origin/<default-branch>` rather than local HEAD, so local commits you haven't pushed would not come with you — implementation would start from a base your partner didn't expect.

```bash
DEFAULT=$(git symbolic-ref --short refs/remotes/origin/HEAD 2>/dev/null | sed 's|^origin/||')
git log --oneline "origin/${DEFAULT}..HEAD"
```

Any output means there are unpushed local commits. Name them and ask whether to push first or start from origin anyway. Don't settle this silently.

**Then check your available tools for a worktree tool:** a name like `EnterWorktree`, `WorktreeCreate`, a `/worktree` command, or a `--worktree` flag. If one exists, use it, named for the slug, and go to Step 4. These tools own directory placement, branch creation, and cleanup.

Such a tool may say it's only for when the user explicitly asks. **They just did:** Step 2 asked where the implementation should run and your partner chose the worktree. That answer is the explicit instruction, and it is your authorization to call the tool now.

**If no native tool exists,** fall back to git:

```bash
git check-ignore -q .worktrees || echo ".worktrees/" >> .gitignore
git worktree add ".worktrees/<slug>" -b "<slug>"
cd ".worktrees/<slug>"
```

Verify the ignore rule before creating anything. An untracked worktree directory that git can see puts an entire second copy of the repo into the next commit.

Worktrees don't inherit the parent repo's hooks. If `<main-repo>/.git/hooks` holds anything, symlink it, or pre-commit checks that were protecting the work quietly stop running.

If creation fails on a permission error, a sandbox is blocking it. Say so and ask what to do.

### 3b. A new branch here

```bash
DEFAULT=$(git symbolic-ref --short refs/remotes/origin/HEAD 2>/dev/null | sed 's|^origin/||')
git checkout -b "<branch-name>" "origin/${DEFAULT}"
```

Announce the branch and what it was cut from. If creation fails, report why and ask whether to use the current branch instead. Then go to Step 5.

### 3c. This branch

Nothing to do. Say which branch the work will land on, so it's on the record before any commit exists. Then go to Step 5.

## 4. Carry the plan across

**Worktree only.** A worktree is a fresh checkout from a commit, so whatever planning wrote is still in the main checkout. Further, if `.gro/` is untracked, it isn't in git at all.

```bash
mkdir -p .gro/projects
cp -R "<main-checkout>/.gro/projects/<date>-<slug>" .gro/projects/
cp "<main-checkout>/.gro/project-plan-guidance.md" .gro/ 2>/dev/null
cp "<main-checkout>/.gro/design-spec-guidance.md" .gro/ 2>/dev/null
cp "<main-checkout>/.gro/run.json" .gro/ 2>/dev/null
```

Confirm `plan.md` and `issues/` arrived before going further. **Leave the originals where they are.** They're your partner's copy of the design work, and it should survive whatever happens to this worktree.

## 5. Set up and baseline

A worktree is a fresh checkout with no installed dependencies. Run the project's setup — `npm install`, `cargo build`, `uv sync`, `go mod download`, whatever the manifests indicate. In an existing checkout, skip straight to the tests.

Run the test suite either way, and report the working tree, the branch, and the result.

**If the baseline fails, stop and report it.** Every failure for the rest of the run is ambiguous until you know which ones were already there; whether to proceed anyway is your partner's call.

## Quick Reference

| Situation | Action |
|---|---|
| `GIT_DIR` differs from `GIT_COMMON` | Already isolated — skip to Step 5, don't ask |
| Same, but `--show-superproject-working-tree` returns a path | Submodule, not a worktree. Ask |
| Worktree chosen, unpushed commits on HEAD | Name them and ask before entering |
| Worktree chosen, native tool available | Use it (Step 3a) |
| Worktree chosen, no native tool | Git fallback into `.worktrees/`, ignore-gated |
| Worktree created | Copy the plan directory in, leave the originals |
| Permission error on creation | Sandboxed. Work in place, continue |
| New branch chosen | Cut from `origin/<default>`, then Step 5 |
| Baseline tests fail | Stop and report before implementing |

## Common Rationalizations

| Excuse | Reality |
|---|---|
| "The plan will say which working tree to use" | It won't, by design. The decision belongs here, where it's acted on. |
| "I can see I'm not in a worktree" | Run the check. Harness-created isolation looks like an ordinary directory. |
| "Obviously they want a worktree, I'll just make one" | It depends on what they're doing with their editor for the next few hours. Ask. |
| "`git worktree add` is right here and I know it works" | The native tool owns placement and cleanup. Bypassing it strands a worktree your harness can't remove. |
| "The tool says only when the user explicitly asks" | Step 2 asked and they chose it. That is the ask. |
| "`.worktrees/` is surely ignored already" | Run `git check-ignore`. Unignored, it commits the whole tree into itself. |
| "The plan is in git, it'll be there" | `.gro/` may be untracked, and the worktree branches from a commit either way. Copy it. |
| "I'll move the plan so the main checkout stays clean" | Copy it. Those files are your partner's record of the design, and they outlive this branch. |
| "Fresh checkout, baseline tests are a formality" | It's a different base commit than the one you were on. Run them. |

## Red Flags

**Never:**
- Create a worktree inside a worktree
- Use raw git when a native worktree tool exists
- Enter a worktree without checking what it branches from
- Delete the plan directory from the main checkout
- Start implementing on a red baseline without saying so

**Always:**
- Detect first, ask second, act third
- Verify the plan directory arrived before dispatching any executor
- Report the working tree, the branch, and the baseline result
