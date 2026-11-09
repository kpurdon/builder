---
name: setup
description: Inspect builder readiness; install or update Builder-owned agents when explicitly requested.
---

# setup

Follow the [working agreement](../../references/working-agreement.md).

Check installed skills and the capabilities needed for the requested workflow. For Goal or session/worktree readiness, use [Codex controls](../../references/codex.md); for session readiness, inspect the selected integration. For Datadog readiness, use [Datadog guidance](../investigate/references/datadog.md). Report gaps and the smallest useful next action.

Readiness checks are read-only. For monitoring or evidence collection, use [native agent setup](references/agents.md) to inspect the installed role, model availability, Python, and required read CLI. Install, update, remove, or runtime-test agents only within the user's requested setup scope. Report configuration readiness separately from observed named-role execution.
