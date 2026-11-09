# builder

A Codex plugin for engineering work, from exploring an idea to delivering and verifying a change. Use individual skills for focused tasks, or assign a project lead to coordinate work through acceptance.

Describe the task naturally or invoke a skill by name. `setup` requires explicit invocation.

| Skill | Purpose | Example requests |
| --- | --- | --- |
| [setup](skills/setup/SKILL.md) | Check readiness and missing prerequisites. | “Use $setup to check builder readiness.”<br>“Use $setup to check the selected session integration.” |
| [design](skills/design/SKILL.md) | Explore a problem, choose an approach, or plan delivery. | “Is this idea worth building?”<br>“Compare queues and direct calls for this workflow.”<br>“Break this agreed design into testable deliveries and a rollout plan.” |
| [manage](skills/manage/SKILL.md) | Own project coordination through verified acceptance. | “Lead this migration through staging acceptance.”<br>“Own this project until its acceptance criteria pass.” |
| [execute](skills/execute/SKILL.md) | Deliver an agreed change through its assigned finish line. | “Implement the approved design.”<br>“Prepare a handoff brief without launching a session.”<br>“Write a PR description for the final diff.” |
| [investigate](skills/investigate/SKILL.md) | Explain unexpected behavior, impact, and likely causes. | “Why did API latency double?”<br>“Investigate the increase in storage costs.” |
| [validate](skills/validate/SKILL.md) | Check acceptance for a specific revision and environment. | “Verify this revision meets the staging acceptance criteria.”<br>“Confirm the fix eliminates duplicate jobs.” |
| [review](skills/review/SKILL.md) | Assess changes, verify findings, and identify gaps in review coverage. | “Check whether these bot findings are real.”<br>“Review this migration against the agreed compatibility constraints.”<br>“Review these instructions for contradictions.” |
| [monitor](skills/monitor/SKILL.md) | Delegate bounded dependency waits to Terra/low. | “Watch CI for this head and return when it finishes.”<br>“Wait for this revision to reach staging.” |

Monitoring uses native subagents with explicit model selection and fresh context; no personal agent registration or global model-default change is required. Builder owns the monitoring role and helpers. Hosts without model-selectable subagents can run the bounded helper locally with a disclosed fallback. The owner handles findings and runtime acceptance.

Run helper regression tests with `python3 -m unittest discover -s tests -v`.
