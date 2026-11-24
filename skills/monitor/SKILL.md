---
name: monitor
description: Track progress, completion, or failure for rollouts, migrations, and other ongoing work.
---

# monitor

## Owner

- For requested monitoring, post short, regular Markdown updates with current status, what changed, progress and ETA when measurable, and any action needed.
- When native monitoring can’t cover a check, use one read-only subagent [with a deadline](references/observation.md), preferably Builder’s [watcher](../../agents/watcher.toml).
- Hand confirmed failures and their evidence back to the execution owner for authorized recovery with [execute](../execute/SKILL.md).
