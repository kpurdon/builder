---
name: monitor
description: Observe known targets through native watches or bounded evidence workers.
---

# monitor

## Owner

- Prefer one [host-native observation mechanism](../../references/codex.md) per dependency and report material changes, blockers, or verified readiness.
- Use one bounded subagent if needed, with scoped read authority, a named target, a deadline, and a return path under the [observation contract](references/observation.md).
- Check [worker readiness](../setup/references/agents.md) and use the Builder [watcher](../../agents/watcher.toml) when the host supports that role.
- Use the configured read interface and the [wait helper](references/helpers.md) when permitted, [CI evidence collector](references/ci.md), or [Kargo/Argo CD guidance](references/akuity.md) as applicable.
- Retain diagnosis, decisions, and acceptance with the owner, and disclose gaps in observation or resumption.
