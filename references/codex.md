# Codex capabilities

Prefer available native controls over custom orchestration; host instructions govern their use. For session launches, follow the [launch interface](../skills/manage/references/sessions.md#launch-interface).

## Goals

Use Goals proactively for substantial work involving multiple steps, iteration, or waits. An applicable standing Goal request is an explicit request to act: start or reuse the Goal without asking again. A task-specific Goal request works the same way. Skip quick answers and trivial edits unless a Goal is requested.

Call `get_goal` before substantive work. Reuse a matching active Goal; if none is unfinished, call `create_goal` with the agreed delivery endpoint and required acceptance evidence, then verify it is active. Include required review, checks, and any assigned rollout or validation in that endpoint. Set a token budget only when explicitly requested. Resolve conflicting or inactive Goals under host controls before relying on continuation.

If neither standing instructions nor the task request Goals and the host requires an explicit request, suggest one while continuing authorized work. If Goal controls are unavailable, disclose that automatic continuation is unverified.

Carry the user's Goal request and assignment-specific objective into [handoffs](../templates/handoff.md); the receiver checks its own thread's Goal state. Recheck state when resuming. Keep the objective through intermediate milestones, reviewer findings, and watcher returns; a draft PR or finished watch completes the Goal only if it satisfies the agreed endpoint. Call `update_goal` with `complete` only after verifying acceptance evidence. Pending work and user gates remain unfinished; use paused or blocked states only under host lifecycle rules. Goal continuation preserves existing approval gates.

## Sessions and worktrees

For session assignment, handoff, or retirement, use [session operations](../skills/manage/references/sessions.md). Reuse suitable worktrees or isolate changes from the intended base. Native tasks and external launchers must not create duplicate executors for one assignment.
