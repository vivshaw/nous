# Gro 🌱

Gro is a suite of agent skills for software development. An offspring of [obra/superpowers](https://github.com/obra/superpowers) and [ed3dai/ed3d-plugins](https://github.com/ed3dai/ed3d-plugins), Gro has been tweaked with an emphasis on lightwight planning, adversarial review loops, and my own standards for code style, prose, and agent diectives.

## You might like Gro if...

Try Gro if you find the following list of principles compelling:

- Simplicity, directness, and concision above all.
- Rule out as many errors as possible with strict typechecking, linting, and autoformatting.
- Use TDD, so the outcome of a project contains its own verification.
- Start projects with questions, not proposals.
- For design specs, a short PRD with crisp, objective requirements is better for agents than a detailed document full of code.
- For project plans and execution, a lightwight kanban approach (like [the Linear Method](https://linear.app/method))) is excellent for both agents and humans.
- After planning is complete, an agent workflow should support front-to-back autonomous completion when desired.
- The main session should be used only for planning and orchestration. All implementation and research should happen in subagents to preserve context length.
- Review is most effective when carried out by a different agent than the one who wrote the code, and iterated until correctness.

## Setup

At the moment, Gro works best in Claude Code. Support for Codex and OpenCode is coming soon.

### Claude Code

```
/plugin marketplace add vivshaw/gro
/plugin install core@gro
# and style@gro, extra@gro, meta@gro, research@gro
```

### Codex

TBD!

### OpenCode

TBD!

## Using Gro

Ask your agent: "How can I use Gro?"

Gro is built around agent-driven skill invocation. You do not generally need to invoke skills yourself. Your agent will determine which ones are relevant based on context. A good starting point is to ask to brainstorm a project. Your agent will pick up the core RPIR workflow and walk you through it.

## What's Inside

- **[Core](plugins/core/README.md):** An opinionated Research -> Plan -> Implement -> Review workflow
- **[Meta](plugins/meta/README.md):** Skills for working with agents, skills, and context
- **[Style](plugins/style/README.md):** Coding standards & language-specific patterns, covering TypeScript, Go, and Rust
- **[Research](plugins/research/README.md):** Skills for doing research and presenting data
- **[Extra](plugins/extra/README.md):** Miscellaneous agent hooks

Each sub-plugin's README provides more details on what exactly it does and how.

## Development

See [docs/DEVELOPING.md](docs/DEVELOPING.md).