# Gro Extra

Gro Extra is currently a dumping ground for utility hooks that haven't found a better home. These hooks will minorly improve certain aspects of agent work, but are not necessary for the core Gro workflow.

## What's Inside

### Hooks

| Hook | Event | Trigger | What it does |
|---|---|---|---|
| `check-bash-secrets.py` | PreToolUse | Bash | Blocks any bash commands that look like they're about to leak credentials or other secrets. |
| `check-sensitive-file.py` | PostToolUse | Write / Edit | Warns when the agent is about to touch files that commonly contain secrets (`.env`, etc.) |
| `git-command-reminder.py` | PostToolUse | Bash | After a `git status` or `git log`, suggests invoking the `meta:project-context-librarian` agent if the changes affect contracts, APIs, or domain structure. |

## Prerequisites

This plugin's hooks use Python 3.11+, and expects it to be available as `python3`.

## Credits

Gro Extra is derived from [ed3dai/ed3d-plugins](https://github.com/ed3dai/ed3d-plugins) (CC BY-SA 4.0, © Ed Ropple). See `LICENSE.ed3d-plugins`.
