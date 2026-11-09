---
name: monitor
description: Delegate bounded CI, review-arrival, and deployment waits to a low-cost observer while the delivery owner retains decisions and validation.
---

# monitor

Use for an observable delivery dependency expected to need repeated checks. Keep a single quick status check local. This skill authorizes a bounded monitoring subagent within the assignment's existing observation scope; it does not authorize deployments, retries, merges, or external messages.

## Owner

Launch one fresh-context native subagent with the installed role `watcher`, selected through the host's named-agent argument (for example, `agent_type`). Its [agent definition](../../agents/watcher.toml) owns the model, reasoning effort, and worker instructions. Do not supply competing model or effort arguments or change global subagent defaults. The service tier follows the parent.

Choose the observation interface before assigning the watch. Prefer the user's configured delivery integration for rollouts; use the [Akuity MCP contract](references/akuity.md) for Kargo, Argo CD, and delivery flows such as Shipit backed by those resources. The [CLI helper](scripts/wait.py) and [helper contract](references/helpers.md) cover CI, review arrival, and direct Kubernetes Deployments. A helper's workload restriction does not limit what the watcher can observe through MCP.

Pass a short assignment: interface, exact target, success criteria, finite deadline, polling interval, working directory, return destination, and absolute paths to the applicable contract and any helper from this installed package. MCP assignments also identify the configured server and permitted read tools. Do not copy the delivery transcript or embed credentials. Paths belong in each assignment so an installed agent does not retain stale plugin-cache paths.

Check [agent readiness](../setup/references/agents.md) when the role is missing, stale, or has not been verified in the intended client. If the host cannot select named roles, disclose that limitation and perform the bounded observation locally through the same interface; do not substitute a generic worker or translate the agent configuration into spawn overrides. Installing an agent file does not change the current session's tool interface.

The delivery owner retains the assignment. Do other useful work or use native completion waits; do not also poll the dependency or ask the monitor for routine progress. On completion, inspect its evidence and continue authorized work. A review arriving is not review approval, and rollout readiness is not runtime acceptance. Stop or retarget the existing monitor when the target changes; do not leave duplicate watchers running. If the host cannot maintain a wait or deliver its result, disclose the missing resumption mechanism.
