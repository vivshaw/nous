# Gro Core

Gro Core is the heart of Gro. This plugin contains Gro's core Research -> Plan -> Implement -> Review workflow. Additionally, it provides a small set of utility skills and agent definitions that support this workflow.

## What's Inside

### Core Workflow

**Research:**

- `core:design-spec-exploring`: Refines a rough idea into a clearly defined project, using questions, codebase exploration, and web research to flesh it out.
- `core:design-spec-writing`: Writes a project spec as a concise PRD with an emphasis on objective, verifiable requirement statements.

**Plan:**

- `core:project-getting-started`: Begins project planning for an accepted project spec, including spinning up a branch.
- `core:project-writing-plan`: Writes a concise project plan and a project kanban full of tasks. The project spec is a high-level document with an emphasis on defining goals and non-goals, hashing out any core technical architecture that must be decided up front, and sequencing work. All specific features and instructions are put in the task board.

**Implement:**

- `core:execute-implement-a-project`: Executes on a project plan milestone by milestone, dispatching subagents per task, and pausing regularly for user input.
- `core:execute-implement-a-project-autonomously`: Executes a project plan fully autonomously, not pausing for user input.
- `core:execute-test-driven-development`: Applies a strict red -> green -> refactor TDD approach, to be used in both implementation work and bugfixes.
- `core:execute-finishing-a-development-branch`: Provides you options for merging, PRing, or cleaning up the branch when the project is done.

**Review:**

- `core:critique-verifying-completion`: Verifies whether the work that was done actually completes the spec that was provided.
- `core:critique-reviewing-code`: Manages a loop of subagent code reviews and fixes until no more issues are flagged.

### Skills

**Orientation:**

- `core:using-gro`: Teaches agents how to find, use, and explain Gro's skills
- `core:using-generic-agents`: Teaches agents when to dispatch generic subagents, and which to pick.

**Exploration & Research Helpers:**

- `core:explore-investigating-a-codebase`: Efficiently and comprehensively explores a codebase and its patterns.
- `core:explore-researching-on-the-internet`: Efficiently and comprehensively explores a topic on the web.
- `core:explore-systematic-debugging`: Applies a structured root-cause analysis to determine the source of a reported bug.

**Prose:**

- `core:prose-writing-for-a-technical-audience`: Guidance for prose clarity in docs, commit messages, and explanations.

**Entrypoints:**

- `core:yoloproject`: A front-to-back workflow for autonomous project work. (More on this below!)

### Agents

- `core:general-purpose-haiku` / `core:general-purpose-sonnet` / `core:general-purpose-opus`: Generic agents, at three model tiers.
- `core:researcher-codebase`: Investigates the state of your current codebase.
- `core:researcher-remote-code`: Clones and analyzes external repositories.
- `core:researcher-internet`: Researches a topic on the internet.
- `core:researcher-combined`: Combines codebase and internet research, for more complex explorations.
- `core:executor-task`: Implements a single issue from a project plan.
- `core:executor-review-fixer`: Responds to a code review and fixes the issues it found.
- `core:critic-code-reviewer`: Performs adversarial code review for code quality, bug spotting, and spec adherence.
- `core:critic-test-analyst`: Validates test coverage against a plan's requirements.

### Hooks

| Hook                             | Event            | What it does                                                                                                          |
| -------------------------------- | ---------------- | --------------------------------------------------------------------------------------------------------------------- |
| `reminder-use-generic-agents.sh` | SessionStart     | Reminds the model to invoke `core:using-generic-agents` whenever it dispatches a generic agent                        |
| `reminder-use-skills.sh`         | UserPromptSubmit | Injects a reminder about invoking Gro skills before responding                                                   |
| `continue-autonomous-run.py`     | Stop             | While in Yoloproject mode, prompts the agent to continue and hands it the next task |

## Yoloproject

Yoloproject is an end-to-end autonomous workflow. You work with the agent to define the spec and plan as usual. From that point onward, the agent will run autonomously until every milestone is complete. It will only stop when it can testably verify that the project requirements are satisfied, or when it runs into a blocking problem and can't make forward progress.

For lower-level details, see [the YOLOPROJECT doc](./YOLOPROJECT.md).

## Principles

- Orchestration and planning in the main session, execution and review in subagents.
- Write lightweight planning documents. Avoid writing code in the planning phase. Focus on requirements.
- Write tests, then write code. Verify that the tests can actually fail.
- Use iterative review loops, with the reviewer and fixer agents sharing no context.

## Credits

Gro Core is derived from [obra/superpowers](https://github.com/obra/superpowers) (MIT, © Jesse Vincent) and [ed3dai/ed3d-plugins](https://github.com/ed3dai/ed3d-plugins) (CC BY-SA 4.0, © Ed Ropple). See `LICENSE.superpowers` & `LICENSE.ed3d-plugins`.
