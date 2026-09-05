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
    assert len(skill_files) == 34

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

    assert load_json(".claude-plugin/plugin.json")["version"] == version
    assert load_json(".codex-plugin/plugin.json")["version"] == version
    assert marketplace["metadata"]["version"] == version
    assert {plugin["version"] for plugin in marketplace["plugins"]} == {version}
    assert f"## [{version}]" in (ROOT / "CHANGELOG.md").read_text()


def test_distribution_shape_and_licenses() -> None:
    assert not any(path.is_file() for path in (ROOT / "plugins").glob("**/*"))
    assert not (ROOT / "agents").exists()
    assert not (ROOT / "hooks").exists()
    for license_file in ("LICENSE", "LICENSE.ed3d-plugins", "LICENSE.superpowers"):
        assert (ROOT / license_file).is_file()
    assert (SKILLS / "visualizing-data/assets/fonts/OFL.txt").is_file()
