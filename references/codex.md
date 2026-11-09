# Codex capabilities

Prefer available native controls over custom orchestration; host instructions govern their use. For session launches, follow the [launch interface](../skills/manage/references/sessions.md#launch-interface).

## Goals

For iterative execution or project management, check Goal state at the start. When the user explicitly requests a Goal, including through applicable standing instructions, create it if none is unfinished and verify it is active. Use the agreed delivery endpoint and acceptance evidence as its objective. Reuse a matching active Goal; resolve a conflicting or inactive Goal under host controls before relying on continuation.

Without an explicit request, suggest a Goal when useful and continue authorized work. A plan or promise to keep going does not activate a Goal. If Goal controls are unavailable, disclose that automatic continuation is unverified.

Carry the user's Goal request and assignment-specific objective into [handoffs](../templates/handoff.md); the receiver checks its own thread's Goal state. Keep the objective through intermediate milestones and complete it only against acceptance evidence. Goal continuation preserves existing approval gates and host lifecycle rules.

## Sessions and worktrees

For session assignment, handoff, or retirement, use [session operations](../skills/manage/references/sessions.md). Reuse suitable worktrees or isolate changes from the intended base. Native tasks and external launchers must not create duplicate executors for one assignment.
