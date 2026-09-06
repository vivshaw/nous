from __future__ import annotations

import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
ALLOWED_FRONTMATTER = {
    "allowed-tools",
    "compatibility",
    "description",
    "license",
    "metadata",
    "name",
}
AGENT_PLUGIN_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
AGENT_PLUGIN_KEYS = {
    "$schema",
    "author",
    "description",
    "homepage",
    "keywords",
    "license",
    "name",
    "repository",
    "version",
}


def load_json(path: str) -> dict:
    return json.loads((ROOT / path).read_text())


def frontmatter(path: pathlib.Path) -> dict[str, str]:
    text = path.read_text()
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    assert match, f"{path.relative_to(ROOT)} has no frontmatter"

    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if line and not line.startswith((" ", "\t")):
            key, separator, value = line.partition(":")
            assert separator, f"invalid frontmatter line in {path.relative_to(ROOT)}: {line}"
            fields[key] = value.strip()
    return fields


def test_canonical_skill_inventory() -> None:
    skill_files = sorted(SKILLS.glob("*/SKILL.md"))
    assert len(skill_files) == 27

    names = []
    for skill_file in skill_files:
        fields = frontmatter(skill_file)
        assert fields.keys() <= ALLOWED_FRONTMATTER
        assert fields.get("name") == skill_file.parent.name
        assert fields.get("description")
        assert len(fields["name"]) <= 64
        assert re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", fields["name"])
        assert len(fields["description"]) <= 1024
        names.append(fields["name"])
    assert len(names) == len(set(names))


def test_release_versions_are_synchronized() -> None:
    package = load_json("package.json")
    version = package["version"]
    marketplace = load_json(".claude-plugin/marketplace.json")
    local_plugin = next(plugin for plugin in marketplace["plugins"] if plugin["name"] == "loam")

    assert load_json("plugin.json")["version"] == version
    assert load_json(".claude-plugin/plugin.json")["version"] == version
    assert load_json(".codex-plugin/plugin.json")["version"] == version
    assert marketplace["metadata"]["version"] == version
    assert local_plugin["version"] == version
    assert f"## [{version}]" in (ROOT / "CHANGELOG.md").read_text()


def test_package_identity_is_synchronized() -> None:
    package = load_json("package.json")
    claude_plugin = load_json(".claude-plugin/plugin.json")
    codex_plugin = load_json(".codex-plugin/plugin.json")
    portable_plugin = load_json("plugin.json")
    marketplace = load_json(".claude-plugin/marketplace.json")
    codex_marketplace = load_json(".agents/plugins/marketplace.json")

    assert package["name"] == "@vivshaw/loam"
    assert portable_plugin["name"] == "loam"
    assert claude_plugin["name"] == "loam"
    assert codex_plugin["name"] == "loam"
    assert marketplace["name"] == "loam"
    assert codex_marketplace["name"] == "loam"
    assert {plugin["name"] for plugin in marketplace["plugins"]} == {"loam", "loam-meta"}
    assert {plugin["name"] for plugin in codex_marketplace["plugins"]} == {
        "loam",
        "loam-meta",
    }
    assert marketplace["renames"]["gro"] == "loam"
    assert marketplace["renames"]["meta"] == "loam-meta"


def test_portable_plugin_manifest() -> None:
    plugin = load_json("plugin.json")

    assert plugin["$schema"] == AGENT_PLUGIN_SCHEMA
    assert plugin.keys() == AGENT_PLUGIN_KEYS
    assert plugin["repository"] == "https://github.com/vivshaw/loam"


def test_pi_package_registration() -> None:
    package = load_json("package.json")

    assert package["pi"]["skills"] == ["./skills"]
    assert "pi-package" in package["keywords"]


def test_distribution_shape_and_licenses() -> None:
    assert not any(path.is_file() for path in (ROOT / "plugins").glob("**/*"))
    assert not (ROOT / "agents").exists()
    assert not (ROOT / "hooks").exists()
    for license_file in ("LICENSE", "LICENSE.ed3d-plugins", "LICENSE.superpowers"):
        assert (ROOT / license_file).is_file()
    assert (SKILLS / "visualizing-data/assets/fonts/OFL.txt").is_file()
    extracted = {
        "maintaining-project-context",
        "managing-a-skills-package",
        "prompt-security-hardening",
        "testing-skills-with-subagents",
        "writing-agent-directives",
        "writing-agents-md-files",
        "writing-skills",
    }
    assert not extracted & {path.parent.name for path in SKILLS.glob("*/SKILL.md")}
