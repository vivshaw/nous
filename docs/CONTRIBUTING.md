# Developing Loam

Loam has one canonical `skills/` tree and thin package metadata for Agent Plugins clients, Claude Code, Codex, OpenCode, and Pi.

Use Loam with its separate Loam Meta, Loam Code, and Loam Research expansion packs.

## Prerequisites

- [Nix](https://nixos.org/download) with flakes enabled
- [direnv](https://direnv.net/) for optional automatic activation

Enter the environment with direnv or `nix develop`, then run `uv sync --all-groups` and `pre-commit install`.

## Commands

| Command | Purpose |
|---|---|
| `uv run pytest` | Run repository tests |
| `uv run ruff check skills/ tools/` | Lint Python |
| `uv run ruff format --check skills/ tools/` | Check formatting |
| `uv run mypy` | Typecheck Python |
| `npm pack --dry-run` | Inspect OpenCode package contents |

## Skills

Each `skills/<name>/SKILL.md` follows the Agent Skills specification. Keep names globally unique and equal to the parent directory. Supporting scripts, references, prompt templates, and assets stay beside their skill.

Canonical skill prose should name capabilities, not host-specific tool or agent identifiers. Platform-specific metadata belongs in manifests or adapters, not generated copies of skills.

## Packaging

- Agent Plugins clients load the root `plugin.json` and canonical `skills/` tree.
- Claude Code discovers root `skills/` through `.claude-plugin/plugin.json`.
- Codex uses `.codex-plugin/plugin.json` and the same root tree.
- OpenCode loads `@vivshaw/loam`; `opencode.js` appends the packaged `skills/` path to live config.
- Pi installs the Git repository or npm package and reads `pi.skills` from `package.json`.

After changing `opencode.js`, restart OpenCode before testing because plugins are loaded at startup.
