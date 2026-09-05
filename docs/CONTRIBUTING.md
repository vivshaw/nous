# Developing Gro

Gro has one canonical `skills/` tree and thin package metadata for Claude Code, Codex, and OpenCode.

Use Gro to develop Gro. Relevant authoring skills include `writing-skills`, `testing-skills-with-subagents`, `writing-agent-directives`, and `managing-a-skills-package`.

## Prerequisites

- [Nix](https://nixos.org/download) with flakes enabled
- [direnv](https://direnv.net/) for optional automatic activation

Enter the environment with direnv or `nix develop`, then run `uv sync --all-groups` and `pre-commit install`.

## Commands

| Command | Purpose |
|---|---|
| `uv run pytest` | Run Python and browser-backed tests |
| `uv run ruff check skills/ tools/` | Lint Python |
| `uv run ruff format --check skills/ tools/` | Check formatting |
| `uv run mypy` | Typecheck Python |
| `uv run python tools/visualizing-data/build_swatches.py --check` | Verify the generated visualization reference |
| `npm pack --dry-run` | Inspect OpenCode package contents |

Install Playwright's isolated Chromium with `uv run playwright install chromium` when browser tests request it.

## Skills

Each `skills/<name>/SKILL.md` follows the Agent Skills specification. Keep names globally unique and equal to the parent directory. Supporting scripts, references, prompt templates, and assets stay beside their skill.

Canonical skill prose should name capabilities, not host-specific tool or agent identifiers. Platform-specific metadata belongs in manifests or adapters, not generated copies of skills.

## Packaging

- Claude Code discovers root `skills/` through `.claude-plugin/plugin.json`.
- Codex uses `.codex-plugin/plugin.json` and the same root tree.
- OpenCode loads `@vivshaw/gro`; `opencode.js` appends the packaged `skills/` path to live config.

After changing `opencode.js`, restart OpenCode before testing because plugins are loaded at startup.
