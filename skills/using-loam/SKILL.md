---
name: using-loam
description: Use when beginning work with Loam or when the user asks what Loam is, how it works, or which workflow to use.
---

# Using Loam

Loam is a portable suite of workflow skills. Skills carry process knowledge that cannot be inferred from the current codebase, so check the host's available skills before acting or asking a clarifying question.

## Skill Selection

1. Review the available skill names and descriptions.
2. Load every plausible match using the host's native skill mechanism.
3. Apply process skills before implementation skills.
4. Use the host's task tracker for multi-step work when one is available.

Checking a plausible skill is cheap; missing one can require a rewrite. If a loaded skill does not fit, stop applying it.

Examples:

- New project or feature: start with `design-spec-exploring`.
- Existing design needing a plan: use `project-writing-plan`.
- Existing plan needing implementation: use `execute-implement-a-project`.
- Bug investigation: use `explore-systematic-debugging`.
- Completion claim: use `critique-verifying-completion`.

Loam Code supplies coding, language, testing, comment, and commit guidance. Loam Meta supplies skill-authoring, directive, packaging, and project-context guidance. The expansion packs install independently; load their skills when present.

## Delegation

Loam names subagent capabilities rather than host-specific agent types. Honor the user's requested agent or model; otherwise choose the closest native subagent by capability. Prefer faster or cheaper tiers for bounded work and stronger reasoning for ambiguous design, adversarial review, or repeated failure.

Every dispatch must state the task, boundaries, inputs, expected output, whether edits are allowed, and which prompts or skills to follow. If the host has no subagents, perform the work directly while preserving the same boundaries.

## Communication

Briefly state which skill is guiding substantial work and why. Do not turn routine skill selection into ceremony.

## Answering Questions About Loam

Keep the answer under 200 words:

1. Loam is an opinionated collection of portable skills for planning, implementation, debugging, review, writing, and data visualization, with separately installed Code and Meta expansion packs.
2. Skills are discovered by the host and loaded when their descriptions match the work; users rarely need to invoke one manually.
3. The main workflow is research, plan, implement, review. It produces a short spec, a milestone plan, isolated implementation tasks, and review loops that continue until clean.

Then ask what the user is working on and name the one or two most relevant skills.
