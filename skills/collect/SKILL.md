---
name: collect
description: Delegate gathering CI failure evidence for an exact PR head to a bounded collector before diagnosis or fixes.
---

# collect

Use when gathering CI failure evidence would require several reads or substantial logs. Keep a single quick lookup local. This skill authorizes one bounded evidence-collection subagent within the assignment's existing read scope.

Select the native `collector` role with a fresh context and no model or effort overrides; its [definition](../../agents/collector.toml) owns execution settings and worker instructions. Supply repository, PR number, exact head SHA, an absolute new local output directory, deadline, collection limits, return destination, and absolute paths to the [helper](scripts/ci.py) and its [contract](references/ci.md) from the installed package. Use [agent setup](../setup/references/agents.md) when role discovery is unavailable; disclose a local-helper fallback rather than silently using a generic expensive agent.

The parent retains diagnosis, fixes, and acceptance. Do useful independent work or wait for native completion; do not fetch the same checks and logs in parallel. Use the returned packet and local artifacts before repeating reads. If evidence is partial, narrow any follow-up to the named gap. A changed head or rerun requires reassessing the target. Do not treat successful collection as successful CI.

This version collects GitHub Actions failure evidence, with links and explicit gaps for other check providers. Review preparation, code reconnaissance, and executing validation commands are outside this role's current scope.
