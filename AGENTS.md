# AGENTS.md

Working guide for `loam`, viv shaw's portable Agent Skills package.

## What This Repo Is

Loam is a package containing 34 skills for research, planning, implementation, review, coding standards, prose, skill authoring, and data visualization. It's compatible with at least OpenCode, Claude Code, and Codex.

## Structure

- `skills/`: canonical skill definitions.
- `.claude-plugin/`: Claude Code manifest and repository marketplace.
- `.codex-plugin/plugin.json`: Codex manifest pointing at `skills/`.
- `opencode.js` and `package.json`: dependency-free OpenCode npm adapter and package metadata.
- `tools/`: repository maintenance scripts.

## Licensing

The package is CC BY-SA 4.0. Preserve all applicable notices when importing or adapting material:

- Original content: `LICENSE`
- Material from ed3dai/ed3d-plugins: `LICENSE.ed3d-plugins`
- Material from obra/superpowers: `LICENSE.superpowers`
- Inter typeface: `skills/visualizing-data/assets/fonts/OFL.txt`

Keep the README Credits section current.

## Required Tooling

Use Loam to develop Loam. Relevant authoring skills include `writing-skills`, `testing-skills-with-subagents`, `writing-agent-directives`, and `managing-a-skills-package`.

The Python and browser toolchain supports data-visualization assets and repository checks. See `docs/CONTRIBUTING.md`.

Never launch an installed browser binary directly. Use Playwright's isolated browser. On macOS, launching an installed browser executable while it is open can hand the command to the user's live browser session.

## Adding Skills

1. Use `writing-skills` and `testing-skills-with-subagents`.
2. Create `skills/<name>/SKILL.md` with Agent Skills-compatible `name` and `description` frontmatter.
3. Keep substantive behavior portable; isolate unavoidable host behavior in a thin adapter.
4. Use bare globally unique skill names in references.
5. Update the README contents and preserve upstream licenses.

Do not add custom agents. Put delegated behavior in a skill or adjacent prompt resource and use each host's native generic subagents.

## Committing And Releasing

- Use Conventional Commits with a scope, following recent history.
- Keep `CHANGELOG.md` in Keep a Changelog format. Use `repo`, `skills`, `claude`, `codex`, or `opencode` scopes as appropriate. Keep descriptions concise.
- Follow Semantic Versioning. Keep `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `.codex-plugin/plugin.json`, `package.json`, the changelog release, and tag synchronized.
- Use `managing-a-skills-package` for packaging and release work.
