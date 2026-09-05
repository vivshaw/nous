# Host Adapters

Check current official documentation before using these examples. Keep package names and versions synchronized with the canonical package.

## Claude Code

Put plugin metadata in `.claude-plugin/plugin.json`. Root `skills/` is discovered automatically.

For repository marketplace distribution, `.claude-plugin/marketplace.json` needs a marketplace `name`, an `owner.name`, and a `plugins` array. Each plugin needs a `name` and a `source`; a package at the repository root uses `"source": "./"`. Add `version`, `description`, licenses, and rename mappings when applicable.

Validate and smoke-test:

```text
claude plugin validate . --strict
/plugin marketplace add owner/repository
/plugin install plugin-name@marketplace-name
```

Open a clean session and confirm every packaged skill is discoverable and its adjacent resources resolve.

## Codex

Put metadata in `.codex-plugin/plugin.json` and point `skills` at `./skills/`. When using a compatible repository marketplace, add and install it with:

```bash
codex plugin marketplace add owner/repository
codex plugin add plugin-name@marketplace-name
```

Open a clean Codex session and confirm the installed version and complete skill inventory. Treat successful marketplace parsing without skill discovery as failure.

## OpenCode

Publish an npm package whose entry point exports a plugin. Its config hook should append the package's absolute `skills/` directory to `config.skills.paths` without duplicating it.

Inspect the package before publication:

```bash
npm pack --dry-run --json
npm publish --dry-run --json
```

For a published package, add it to an isolated `opencode.json`:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "plugin": ["@owner/package"]
}
```

Run `opencode debug config` and `opencode debug skill`. The resolved config must contain the packaged absolute skill path, and the discovered names and count must match the archive.
