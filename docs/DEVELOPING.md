# Developing Gro

Are you interested in contributing to Gro, or developing your own fork? This document will provide what you need.

## Prerequisites

- [Nix](https://nixos.org/download) (with flakes enabled)
- [direnv](https://direnv.net/) (optional, for auto-activation)

All other developer tools you'll need are pinned in the Nix flake.

### Up and Running

If you have direnv active, you will be prompted to `direnv allow` upon `cd`ing in. If you do not, use `nix develop` to enter a one-off Nix shell. Once you are in the shell, run `pre-commit install` to activate Git hooks.

### Developing Hooks

Some Gro features are implemented as hooks. The hooks relevant to the core workflow live in [Gro Core](../plugins/core/). Assorted others live in [Gro Extra](../plugins/extra/). At this time, the preferred language for hooks is Python. Shell is also acceptable, but only for extremely simple scripts only.

If written in Python, you should include tests for your hook implementation.

### Python Toolchain

Dev deps are managed by [uv](https://docs.astral.sh/uv/).

| Command | What it does |
|---|---|
| `uv run pytest` | run the hook tests |
| `uv run ruff check plugins/` | lint |
| `uv run ruff format plugins/` | format |
| `uv run mypy` | typecheck |

Config lives in:

- `flake.nix`: pinned tool versions
- `pyproject.toml`: uv deps, ruff / mypy / pytest config
- `.pre-commit-config.yaml`: git hook config
