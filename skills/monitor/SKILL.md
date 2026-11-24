---
name: monitor
description: Track progress, completion, or failure for rollouts, migrations, and other ongoing work.
---

# monitor

## Owner

- Post short, regular Markdown updates with current status, what changed, progress and ETA when measurable, and any action needed.
- Use one read-only subagent for a [specific check with a deadline](references/observation.md) when native monitoring can’t cover it.
- Use Builder’s [watcher](../../agents/watcher.toml) role when available.
- Hand confirmed failures and their evidence back to the execution owner for authorized recovery with [execute](../execute/SKILL.md).
