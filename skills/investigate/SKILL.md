---
name: investigate
description: Explain unexpected behavior, incidents, performance, or cost.
---

# investigate

Follow the [working agreement](../../references/working-agreement.md).

Find evidence that distinguishes causes and connects them to impact. Surface useful mitigation before full causal certainty; an explanation does not finish assigned recovery.

For CI failures needing several reads or substantial logs, use [collect](../collect/SKILL.md) to gather revision-pinned evidence before diagnosis.

Check environment and dependency ownership before local diagnostics; package runners and imports can change environments or contact services. Isolate uncertain effects. Before scaling a synthetic experiment, trial a representative case for isolation, version compatibility, and capacity. Keep language-specific setup in repository guidance and conclusions within the fixture's limits.

Carry assigned interventions through delivery and verify their effects. For interventions, rollout, recovery, or operational artifacts, use [operational procedures](../execute/references/operations.md). For Datadog work, use [Datadog guidance](references/datadog.md).
