---
name: monitor
description: Observe known targets through host-native watches or bounded evidence workers while the owner retains diagnosis, decisions, and validation.
---

# monitor

Use when observing a known target requires repeated checks or several reads to gather evidence. The assignment may be a snapshot, a wait, or a wait followed by evidence capture. Keep a single quick lookup local. When a worker is needed, this skill authorizes one bounded subagent within the assignment's existing read scope; it does not authorize deployments, workflow reruns, fixes, or external messages.

## Owner

Prefer the host's native watch and completion mechanisms. Follow its rules for PR linkage, wakeups, delegated-work completion, and cancellation; do not run a polling worker alongside a native watch for the same target. A wakeup prompts reassessment of the current target, not acceptance.

Use a bounded worker for evidence gathering or observation that needs one. Select the host-supported mechanism after checking [worker readiness](../setup/references/agents.md). For Codex named agents, select the installed `watcher` role with fresh context; its [definition](../../agents/watcher.toml) owns model, reasoning effort, and worker instructions. Other hosts may use their delegation controls with the same [observation contract](references/observation.md). Follow the host's runtime selection and inheritance rules rather than assuming Codex defaults or changing global settings.

Define the observation question and expected evidence. Supply the exact target and applicable revision/attempt/environment/time window, read interface, finite deadline, limits, working directory, return destination, and any local artifact destination. For a wait, include its predicate, interval, and stop conditions; for wait-then-capture, reserve capture time within the same overall deadline. Give absolute paths to the applicable contracts and helpers from this installed package. Do not copy the delivery transcript or embed credentials.

Choose the read interface from the user's configured integrations and available tools. When the host permits polling and no native watch covers the wait, use a deterministic helper if it covers the assignment; otherwise use scoped read tools under the [observation contract and examples](references/observation.md). Evidence helpers can also gather a bounded snapshot after a native wakeup. Helper coverage does not limit the role to a particular provider or workload type.

- [Wait helper](references/helpers.md): CI checks, submitted review arrival, and direct Kubernetes Deployments.
- [CI evidence helper](references/ci.md): failed-check/job/log collection for an exact GitHub Actions PR head, independently or after a wait.
- [Kargo/Argo CD MCP](references/akuity.md): Kargo/Argo/Shipit observation through the configured delivery integration, including owner-run [MCP/CLI login refresh](references/akuity.md#login-refresh).

The owner retains diagnosis, fixes, decisions, and acceptance. Follow the host's return and resumption instructions; do not poll delegated tasks or duplicate worker reads for progress. Use returned evidence before refetching, and narrow any follow-up to the named gap. Stop or retarget observation through the host's supported controls when the target changes. Evidence gathered, a review arriving, a promotion succeeding, and runtime acceptance are separate outcomes.

If neither native observation nor a suitable worker is available, disclose a local observation fallback permitted by the host; do not silently substitute an expensive worker. The owner handles expired credentials and resumes only within the remaining deadline. Identify any unsupported deadline, wakeup, or resumption requirement and the actual return path.
