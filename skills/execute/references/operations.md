# Operational procedures

Use repository delivery mechanisms; scale rollout, observation, and recovery planning to risk.

## Interventions and rollout

Establish the target, expected effect, recovery path, and stop conditions. Verify the intended artifact and configuration across the affected serving population, then test behavior; healthy older revisions prove nothing.

On failure, a new failure mode, or a superseding deployment, stop progression and reassess before retrying or expanding scope.

## Observation and recovery

Keep an owner and stopping condition for observation. Measure recovery in the failed population and behavior, including residual work and delayed effects; moving work is not processing it.

Distinguish restoration, cause, durable repair, and remaining recovery. Reconcile emergency changes with their source of truth.

## Operational artifacts

Prepare human-run commands and queries for the actual client and target. Use available context; ask when either is unknown. Explain client or connection limits, including session settings that may not survive separate submissions.

Preserve useful existing content and verify saved behavior, including representative queries and rendering. Investigate unexpected readback before retrying. For Datadog artifacts, use [Datadog guidance](../../investigate/references/datadog.md).
