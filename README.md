# builder

A Codex plugin for engineering work, from exploring an idea to delivering and verifying a change. Use individual skills for focused tasks, or assign a project lead to coordinate work through acceptance.

Describe the task naturally or invoke a skill by name. `setup` requires explicit invocation. Readiness inspection is read-only; agent installation and updates must be requested explicitly.

| Skill | Purpose | Example requests |
| --- | --- | --- |
| [setup](skills/setup/SKILL.md) | Check readiness and install requested agent definitions. | “Use $setup to check builder readiness.”<br>“Use $setup to check the selected session integration.” |
| [design](skills/design/SKILL.md) | Explore a problem, choose an approach, or plan delivery. | “Is this idea worth building?”<br>“Compare queues and direct calls for this workflow.”<br>“Break this agreed design into testable deliveries and a rollout plan.” |
| [manage](skills/manage/SKILL.md) | Own project coordination through verified acceptance. | “Coordinate the owners delivering this migration.” |
| [execute](skills/execute/SKILL.md) | Deliver an agreed change through its assigned finish line. | “Own this change through staging acceptance.”<br>“Prepare a handoff brief.” |
| [investigate](skills/investigate/SKILL.md) | Explain unexpected behavior, impact, and likely causes. | “Why did API latency double?”<br>“Investigate the increase in storage costs.” |
| [validate](skills/validate/SKILL.md) | Check acceptance for a specific revision and environment. | “Verify this revision meets the staging acceptance criteria.”<br>“Confirm the fix eliminates duplicate jobs.” |
| [review](skills/review/SKILL.md) | Assess changes, verify findings, and identify gaps in review coverage. | “Check whether these bot findings are real.”<br>“Review this migration against the agreed compatibility constraints.”<br>“Review these instructions for contradictions.” |
| [monitor](skills/monitor/SKILL.md) | Observe targets through native watches or bounded evidence workers. | “Watch CI for this head and return when it finishes.”<br>“Wait for this revision to reach staging.”<br>“Gather review feedback or logs for this exact target.” |

Observation prefers the host's native watches and completion mechanisms, including in T3. Bounded workers gather evidence under one [observation contract](skills/monitor/references/observation.md); the owner handles findings and runtime acceptance. [Worker readiness](skills/setup/references/agents.md) checks host delegation as well as named roles. For Codex named agents, Builder owns the [watcher definition](agents/watcher.toml), and setup installs or refreshes it while preserving local edits. Plugin updates alone do not refresh that separate registration. Rollout watches prefer the user's configured delivery integration, including [Akuity MCP](skills/monitor/references/akuity.md). CLI helpers cover host-permitted polling and [CI failure evidence](skills/monitor/references/ci.md).

Run helper regression tests with `python3 -m unittest discover -s tests -v`.

Managed initiatives use explicit session membership independent of directories and UI groups. [Session operations](skills/manage/references/sessions.md) define ownership and interface selection; a selected integration such as [dispatcher](https://github.com/kpurdon/dispatcher) owns native mechanics and its local registry. Broad discovery can stay in a parent workspace while repository-specific executors use isolated worktrees as scope becomes known.
