---
name: managing-a-skills-package
description: Use when creating, adapting, validating, auditing, or releasing a portable Agent Skills package for one or more agent hosts.
---

# Managing a Skills Package

Treat skills and their adjacent resources as the product. Manifests, marketplaces, and loaders are thin host adapters around one canonical `skills/` tree.

## Load Supporting Guidance

Load only what the task needs:

- `writing-skills` when creating or changing a `SKILL.md`.
- `testing-skills-with-subagents` when testing changed skill behavior.
- `writing-agent-directives` when writing orchestration or delegated prompt resources.
- The repository's release and changelog guidance before preparing a release.

## Package Shape

```text
package/
  skills/
    my-skill/
      SKILL.md
      references/
      scripts/
      assets/
  .claude-plugin/plugin.json
  .claude-plugin/marketplace.json # only for marketplace distribution
  .codex-plugin/plugin.json
  package.json              # only when an npm adapter is needed
  opencode.js               # optional skill-path registration
  README.md
  LICENSE
```

Keep canonical skill content provider-neutral. Name capabilities rather than exact tools, native subagent roles rather than custom agent identifiers, and user interaction rather than one host's question API.

Do not generate skill copies per host, add a registry for fields that appear once, or ship custom agents or lifecycle hooks. Put delegated behavior in skills or adjacent prompt resources. Add an MCP server only when the workflow requires a capability the host cannot otherwise provide.

## Add Only Necessary Adapters

- **Claude Code:** Add `.claude-plugin/plugin.json`; root `skills/` is natively discovered. For repository distribution, add a marketplace whose plugin source starts with `./` and resolves inside the package.
- **Codex:** Add `.codex-plugin/plugin.json` pointing `skills` at `./skills/`. Add marketplace metadata when that is the chosen installation path.
- **OpenCode:** For npm distribution, export a small plugin whose `config` hook appends the packaged `skills/` path to `config.skills.paths`.

Consult current official documentation before editing an adapter. Host schemas evolve independently of the Agent Skills specification.

Read the adjacent `host-adapters.md` only for the hosts being added, validated, or released. It contains minimal manifest fields, install commands, and discovery checks.

## Validate

1. Validate every `SKILL.md` against the Agent Skills specification.
2. Confirm names match directories and are globally unique.
3. Check relative resources and links.
4. Run repository tests and validate each host manifest.
5. Inspect the archive or npm tarball for every skill resource and applicable license.
6. Smoke-test clean installation and skill discovery on every advertised host.

Use each host's current validator. Typical checks include `uvx --from skills-ref agentskills validate skills/<name>`, `claude plugin validate . --strict`, and `npm pack --dry-run --json`. Test Codex and OpenCode with isolated installs when no stable manifest validator is available.

Automate small checks for skill inventory and synchronized metadata. Do not create a generator merely to synchronize a few scalar fields.

## Release

When preparing a release:

1. Choose the Semantic Version from the behavioral change, including host-specific breakage.
2. Apply it to every present manifest, marketplace entry, and package file.
3. Finalize the changelog with user-visible additions, changes, fixes, removals, and migration steps.
4. Run the complete validation sequence above.
5. Inspect the final archives and confirm every version, resource, executable, and license.
6. Smoke-test clean installation and discovery on every supported host.
7. Confirm the changelog release, metadata, and intended tag are identical.
8. Commit, tag, or publish only when explicitly requested.

One release has one version across every host.
