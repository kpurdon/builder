# Session operations

For assigned projects, apply the [project management execution boundary](../SKILL.md). Otherwise, keep short or coupled work local; separate sessions need ready assignments and a benefit exceeding coordination cost. Prefer bounded subagents for supporting contributions.

Prepare handoffs with the [brief](../../../templates/handoff.md), linking artifacts rather than transcripts. Use the [selected launch interface](#launch-interface) for authorized launches.

Carry established scope and authority into the brief. Distinguish acceptance evidence from approval gates; a new delivery stage is not itself a user gate. For each gate, identify the concrete action and the restriction, missing authority, or consequential decision requiring user input. Reconcile claimed gates with the original request and current governing instructions; continue covered work, including bounded validation, without renewed approval.

## Receiver selection

Continue the verified current owner when a delivery advances stages or resumes after a wait. Use fresh sessions for new deliveries unless the user selects an existing thread; matching titles or idle status are insufficient evidence of ownership. User-selected threads need identity and scope checks, not recent ownership evidence.

## Ownership and observation

Launch only within established authority; a brief-only request does not authorize a launch. A delegated launcher owns one launch, not delivery or further handoffs.

Give each managed initiative a stable ID and one authoritative membership inventory, independent of UI grouping. With a scoped integration such as Dispatcher, keep its registry outside repositories and reference it from the [project record](../../../templates/project.md); do not duplicate member lists there. Record the lead's verified native identity. Without such an integration, the project record owns the explicit member inventory; never reconstruct it by searching all sessions.

Before dispatch, assign one owner and reserve the assignment through the selected integration. Carry initiative, member, request, registry, and lead references into the brief. Keep backend, native conversation, terminal, and UI group IDs distinct. Record launch, grouping, startup, and delivery evidence separately; leave unobserved startup unconfirmed. Silence or queued messages prove neither success nor failure.

List, inspect, message, and retire initiative members through that inventory and the selected integration's scope checks. A shared repository, directory, title, PR, or UI group does not establish membership. Adopt an existing session only with explicit user selection or an authorized transfer and verified native identity. A concrete dependency blocker involving an outside owner permits only the established blocker interaction; it does not grant management authority over their session.

Uncertain launches may already be running: preserve the prompt, original request, and returned IDs and reconcile on the same backend before retrying. Follow the integration's replay contract; correlation IDs alone do not deduplicate. Repair only the failed part of a partially accepted launch. Never create another executor by switching backend, request key, or assignment label to bypass uncertainty.

Transfer only after the former writer stops and a named successor accepts the remaining obligations; record that acceptance and unfinished work before the successor writes. Returning coordination to the lead does not transfer execution ownership. Idle sessions retain their assignments.

Executors use [monitor](../../monitor/SKILL.md) for repeated dependency observation. Leads do not launch a second watcher for the same dependency or request milestone reports.

## Current-state records

Keep delivery coordination in one local project record, separate from the external issue or project. Reference the authoritative membership inventory and integration rather than maintaining a second native session list. Update ownership, prerequisites, acceptance, and next actions where they are owned; avoid duplicating updates across briefs, the registry, and records. Distinguish the delivery endpoint from its next milestone and retain pending gates and resumption triggers.

Linear and other external trackers are not session coordination logs. Add narrative updates only for consequential decisions that future work needs, with the reason and affected scope; update authorized issue fields when actual project state changes. Keep launch IDs, acknowledgements, progress, waits, watcher output, and retirement details local. Tracker-maintenance authority does not require a post for each event. The lead records a shared decision once on the relevant issue; executors do not mirror it across tickets.

## Delivery state and blockers

Executors work independently, maintain delivery artifacts and authorized ticket state, and leave acceptance evidence with those artifacts. No completion report or acknowledgement to the lead is required.

Shared files or nearby work alone do not require coordination. Inspect available code, diffs, PRs, and assignment records; use isolated worktrees and resolve merge conflicts during integration. Do not ask other sessions to confirm prospective edits or file ownership. Contact another execution session only when blocked and unable to proceed without its action, naming the blocked operation and specific action needed; normally bring that blocker to the lead. Continue work that does not depend on the reply.

When resuming or deciding which work is ready, the lead refreshes the linked tickets, PRs, and acceptance evidence. Assess those sources against the assigned finish line: a Done ticket or merged PR establishes completion only when it satisfies that endpoint. Use a linked local artifact for evidence that has no external home. Do not require a message to accept completed work or unblock a dependency, poll owners for status, or duplicate executor-owned watches.

Executors present concrete merge or approval requests directly to the user and bring blockers needing an unavailable decision, authority, or outside help to the user first. A ready PR, unavailable permission, or completed set of available checks does not end ownership when acceptance remains open. Leads contact active owners only to resolve a blocker or convey a necessary change to or cancellation of the assignment.

Use permitted native messaging for blockers. If unavailable, raise the blocker to the user; do not use a tracker as a fallback message bus. Silence alone is not a reason to contact or replace an owner.

## Launch interface

Honor the requested or established launch interface and use its installed integration. Otherwise, prefer available native session capabilities. Supply the assignment and retain returned identifiers in the authoritative membership inventory. If the selected interface is unavailable, resolve the choice before launching a substitute.

For a new initiative, an explicit interface request wins; otherwise verify the originating interface and apply any configured default when origin is unknown. Installed software, tool availability, and inherited environment variables alone do not establish origin. Persist the selection. Existing members retain their recorded backend even when the lead's interface changes; a per-launch override does not migrate other sessions.

Keep launch workspace and target repositories separate. A broad discovery/PM session can start in a parent workspace before affected repositories are known. As scope emerges, bind independent implementation sessions to the appropriate repository worktrees when the selected interface supports it. Give each the relevant shared contracts and dependencies. Do not split coupled cross-repository work solely to fit UI grouping; when preserving a broader launch workspace, keep target worktree paths explicit.

Include any requested title in the brief and pass it at creation when supported. Terminal and native session titles are separate; have the receiver set a requested native title before work and record unavailable title controls locally.

## Retirement

The lead owns retirement after verifying the delivery's acceptance criteria, cancellation of the assignment, or an accepted transfer to a named successor. An intermediate milestone or pending user gate is insufficient. Preserve the outcome, evidence, and any accepted successor obligations in the project record first; confirm no active descendants or unfinished work depend on the session. Verified acceptance does not itself grant cleanup authority.

Within established cleanup authority, close the execution session through the selected interface and its installed integration. Verify the recorded identity and preserve unrelated work sharing its resources. Let the integration own closure mechanics, confirmation, and uncertain-result handling.

Record retirement evidence or the blocker and next action in the project record. If the integration is unavailable or closure is unconfirmed, leave cleanup pending. Archiving a session, closing its runtime, and deleting its worktree are separate operations with separate authority and evidence. Cleanup failure does not undo acceptance.
