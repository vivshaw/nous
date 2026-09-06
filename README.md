# Loam

Loam is a portable suite of Agent Skills for software development. It grew from [obra/superpowers](https://github.com/obra/superpowers) and [ed3dai/ed3d-plugins](https://github.com/ed3dai/ed3d-plugins), with an emphasis on lightweight planning, independent review loops, strict coding standards, clear prose, and durable project state.

## Principles

- Prefer simplicity, directness, and concision.
- Use strict typechecking, linting, formatting, and tests to rule out errors.
- Start projects with questions and write short, verifiable requirements.
- Keep project plans lightweight and use one durable progress record.
- Delegate bounded implementation and research to fresh native subagents when available.
- Have a different context review work than the one that wrote it.

## Install

Loam ships the same `skills/` tree to Claude Code, Codex, and OpenCode. It contains no custom agents or lifecycle hooks.

### Claude Code

```text
/plugin marketplace add vivshaw/loam
/plugin install loam@loam
```

### Codex

```bash
codex plugin marketplace add vivshaw/loam
codex plugin add loam@loam
```

### OpenCode

Add the npm package to `opencode.json`:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "plugin": ["@vivshaw/loam"]
}
```

Restart OpenCode after changing its config.

## Use

Describe the work normally: “plan this feature,” “implement this project plan,” “debug this failure,” or “review this branch.” The host discovers relevant skills from their descriptions. To get oriented, ask: “How can I use Loam?”

The main workflow is research, plan, implement, review. Planning produces `.loam/projects/<project>/spec.md`, `plan.md`, and isolated issue files.

## Contents

- Workflow: design exploration, PRD writing, project planning, implementation, TDD, independent review, debugging, and branch completion.
- Authoring: skills, agent directives, portable packages, marketplaces, and `AGENTS.md` maintenance.
- Coding: TypeScript, React, Go, Python, Rust, PostgreSQL, testing, comments, commits, and defensive design.
- Research and prose: codebase investigation, internet and remote-source research, technical writing, and data visualization.

Every skill and its supporting resources live under `skills/`.

## The `.loam` directory

This directory contains all the planning materials your agent writes. It's up to you whether to commit it to git or ignore it. Personally, I would recommend ignoring it. I think the types of written material that make good project guidance for an agent are very different from the types of written material that makes good durable documentation.

## Development

See [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md).

## Remix Loam

Tune the suite to your own workflow: swap its PRD format, issue tracker, coding standards, review policy, or language guidance. Loam includes skills for maintaining skill suites and agent directives, so the suite can help you change the suite.

## Credits

Loam is licensed under [CC BY-SA 4.0](LICENSE).

- Material adapted from `obra/superpowers` retains its [MIT license notice](LICENSE.superpowers).
- Material adapted from `ed3dai/ed3d-plugins` retains its [CC BY-SA 4.0 license notice](LICENSE.ed3d-plugins).
- The bundled Inter typeface is covered by its adjacent [SIL OFL 1.1 license](skills/visualizing-data/assets/fonts/OFL.txt).
