---
name: monitor
description: Delegate bounded observation and evidence gathering to a low-cost watcher while the owner retains diagnosis, decisions, and validation.
---

# monitor

Use when observing a known target requires repeated checks or several reads to gather evidence. The assignment may be a snapshot, a wait, or a wait followed by evidence capture. Keep a single quick lookup local. This skill authorizes one bounded subagent within the assignment's existing read scope; it does not authorize deployments, workflow reruns, fixes, or external messages.

## Owner

Select the installed native `watcher` role with a fresh context through the host's named-agent argument (for example, `agent_type`). Its [definition](../../agents/watcher.toml) owns model, reasoning effort, and worker instructions. Do not supply competing model or effort arguments or change global defaults. The service tier follows the parent.

Define the observation question and expected evidence. Supply the exact target and applicable revision/attempt/environment/time window, read interface, finite deadline, limits, working directory, return destination, and any local artifact destination. For a wait, include its predicate, interval, and stop conditions; for wait-then-capture, reserve capture time within the same overall deadline. Give absolute paths to the applicable contracts and helpers from this installed package. Do not copy the delivery transcript or embed credentials.

Choose the interface from the user's configured integrations and available tools. Use a deterministic helper when it covers the assignment; otherwise the watcher may use scoped read tools under the [observation contract and examples](references/observation.md). Helper coverage does not limit the role to a particular provider or workload type.

- [Wait helper](references/helpers.md): CI checks, submitted review arrival, and direct Kubernetes Deployments.
- [CI evidence helper](references/ci.md): failed-check/job/log collection for an exact GitHub Actions PR head, independently or after a wait.
- [Akuity MCP](references/akuity.md): Kargo/Argo/Shipit observation through the configured delivery integration, including owner-run [MCP/CLI login refresh](references/akuity.md#login-refresh).

The owner retains diagnosis, fixes, decisions, and acceptance. Do other useful work or wait for native completion; do not duplicate the watcher's reads or ask for routine progress. Use its returned evidence before refetching, and narrow any follow-up to the named gap. Stop or retarget the existing watcher when the target changes. Evidence gathered, a review arriving, a promotion succeeding, and runtime acceptance are separate outcomes.

Check [agent readiness](../setup/references/agents.md) when the role is missing, stale, or unverified in the intended client. If named-role selection is unavailable, disclose a local observation fallback through the same interface; do not silently use a generic expensive worker or copy model settings into spawn overrides. The owner handles expired credentials and resumes only within the remaining deadline. If the host cannot maintain or resume observation, identify the limitation and the actual return path.
