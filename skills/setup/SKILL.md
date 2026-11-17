---
name: setup
description: Inspect builder readiness; install or update Builder-owned agents when explicitly requested.
---

# setup

Follow the [working agreement](../../references/working-agreement.md).

Check installed skills and the capabilities needed for the requested workflow. For Goal or session/worktree readiness, use [host controls](../../references/codex.md); for session readiness, inspect the selected integration. For Datadog readiness, use [Datadog guidance](../investigate/references/datadog.md). Report gaps and the smallest useful next action.

Readiness checks are read-only. For monitoring, use [worker readiness](references/agents.md) to inspect native watches, supported delegation, and any required role, model, helper, or read interface. Install, update, remove, or runtime-test agents only within the user's requested setup scope. Report configuration readiness separately from observed execution.

For managed-session readiness, inspect the selected integration's initiative-scoped listing, verified origin and native identities, pending-request recovery, and supported launch/message/retirement operations. In dispatcher, inspect its skill and run the registry help and isolated temporary-state tests without launching sessions. In T3, distinguish injected native tools from an outside client's configured MCP connection; CLI installation alone does not establish full lifecycle support. Readiness does not adopt existing sessions or migrate an initiative's interface.
