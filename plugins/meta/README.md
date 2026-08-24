# Gro Meta

Gro Meta is Gro's skill suite for working with agents. It contains guidance for writing and testing skills, speccing out agent definitions, working with project context in AGENTS.md files, and authoring Claude Code plugins.

## What's Inside

### Skills

**General:**

- `meta:writing-agent-directives`: How to write token-efficient, high-compliance guidance for agents.
- `meta:prompt-security-hardening`: How to instruct agents to work safely with secrets.

**Skills:**

- `meta:writing-skills`: Guidance for writing clear and effective agent skills.
- `meta:testing-skills-with-subagents`: A TDD-style pressure-testing workflow for agent skills.

**Project context:**

- `meta:writing-agents-md-files`: How to structure `AGENTS.md` files and what to include in them.
- `meta:maintaining-project-context`: Keeps `AGENTS.md` current as the codebase evolves.

**Agents:**

- `meta:creating-an-agent`: How to write a spec for a new type of agent.

**Distribution:**

- `meta:creating-a-plugin`: Scaffolds a new Claude Code plugin.
- `meta:maintaining-a-marketplace`: Keeps a Claude plugin marketplace healthy during maintenance.

### Agents

- `meta:project-context-librarian`: Updates `AGENTS.md` files in response to project changes.

## Credits

meta is derived from [ed3dai/ed3d-plugins](https://github.com/ed3dai/ed3d-plugins) (CC BY-SA 4.0, © Ed Ropple), which itself draws from [obra/superpowers](https://github.com/obra/superpowers) (MIT, © Jesse Vincent). See `LICENSE.ed3d-plugins` and `LICENSE.superpowers`.
