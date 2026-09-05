# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [6.0.0] - 2026-09-04

### Added

- **skills:** `visualizing-data`, a comprehensive skill for data visualization, including a house palette, style guide, and accessibility checks.
- **tooling:** A pinned Playwright browser for visual checks (`uv run playwright install chromium`).
- **codex:** A native plugin manifest for Codex.
- **opencode:** A dependency-free npm adapter that registers Gro's canonical skill path.

### Changed

- **repo:** BREAKING: Gro is now one package containing one canonical root `skills/` tree for Claude Code, Codex, and OpenCode. Install `gro@gro` instead of separate marketplace plugins.
- **skills:** Merged `project-getting-started` into `project-writing-plan`, which now owns planning input selection and execution handoff.
- **skills:** Implementation now offers a worktree, new branch, or current branch and preserves provenance-aware cleanup behavior.
- **skills:** `using-gro` now explicitly answers “how do I use Gro?”
- **skills:** Project materials moved from `.gro/tasks/` to `.gro/projects/`.
- **skills:** TypeScript tooling guidance now covers stricter static analysis and TypeScript 7.
- **skills:** Consolidated package creation and marketplace maintenance into `managing-a-skills-package`, which loads narrower authoring guidance only when needed.
- **skills:** Portable implementer and review-fixer prompts now require complete scope delivery and load `writing-comments` when comments change.

### Fixed

- **tooling:** `.venv` console scripts pointed at an outdated path, breaking local tools. Now regenerated.
- **skills:** The implementer prompt now loads the existing `critique-verifying-completion` skill instead of a nonexistent verification skill.

### Removed

- **repo:** BREAKING: Removed the five-plugin layout and generated per-platform copies.
- **repo:** BREAKING: Removed custom agents, model aliases, secret-protection hooks, stop-continuation hooks, and skills about them.
- **skills:** Removed `yoloproject` and `execute-implement-a-project-autonomously` together with their autonomous-mode documentation.

## [5.0.0] - 2026-08-24

### Added

- **style:** A `howto-code-in-python` skill covering Python guidance.

### Changed

- **style:** Revised TypeScript guidance to prefer Zod for runtime types and voidzero ecosystem tools for testing, linting, and formatting. The TypeBox reference is replaced by a Zod one.
- **repo:** Rewrote the README and every plugin README for clarity, and split the autonomous-run walkthrough out into `plugins/core/YOLOPROJECT.md`.

### Removed

- **style:** The `using-functional-core-imperative-shell` skill is gone. Anything that dispatched it — `style:coding-effectively`, `core:executor-task`, `core:critic-code-reviewer`, and the TypeScript guidance — no longer does.

## [4.0.1] - 2026-08-19

### Fixed

- **core:** Codebase research is now scoped to the current project unless explicitly asked. A design for a fresh project no longer picks up patterns from unrelated repos on the machine.

## [4.0.0] - 2026-08-19

### Changed

- **repo:** Renamed from loam to gro. The marketplace is now `gro`, so installs are `/plugin install core@gro` and existing users need to re-add the marketplace.
- **core:** The state directory moved from `.loam/` to `.gro/`. In-flight work under `.loam/` is not migrated — move the directory by hand, or re-plan.
- **core:** `using-loam` is now `core:using-gro`.

## [3.0.0] - 2026-08-19

### Changed

- **core:** The project planning workflow is dramatically simplified. A project plan is now one `plan.md` plus one file per issue under `issues/`.

## [2.1.0] - 2026-08-18

### Added

- **style:** A new `howto-code-in-go` skill.

## [2.0.0] - 2026-08-16

### Added

- **core:** A new `design-spec-exploring` skill, covering the ideation and research process for a PRD.
- **repo:** Added this changelog and adopted semver.

### Changed

- **core:** `design-spec-getting-started`, `design-spec-asking-clarifying-questions`, and `design-spec-brainstorming`, are all folded into `design-spec-exploring`
- **core:** `design-spec-writing` now produces a more concise PRD-style spec.
- **core:** `project-writing-plan` now derives its own phase breakdown from the spec's requirements, using the priority levels for scoping.
- **meta:** `maintaining-a-marketplace` now treats its changelog format as a default a project can override

## [1.0.0] - 2026-02-16

### Added

- Initial marketplace: the `core`, `meta`, `style`, and `extra` plugins
