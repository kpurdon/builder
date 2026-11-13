# Session operations

For assigned projects, apply the [project management execution boundary](../SKILL.md). Otherwise, keep short or coupled work local; separate sessions need ready assignments and a benefit exceeding coordination cost. Prefer bounded subagents for supporting contributions.

Prepare handoffs with the [brief](../../../templates/handoff.md), linking artifacts rather than transcripts. Use the [selected launch interface](#launch-interface) for authorized launches.

Carry established scope and authority into the brief. Distinguish acceptance evidence from approval gates; a new delivery stage is not itself a user gate. For each gate, identify the concrete action and the restriction, missing authority, or consequential decision requiring user input. Reconcile claimed gates with the original request and current governing instructions; continue covered work, including bounded validation, without renewed approval.

## Receiver selection

Continue the verified current owner when a delivery advances stages or resumes after a wait. Use fresh sessions for new deliveries unless the user selects an existing thread; matching titles or idle status are insufficient evidence of ownership. User-selected threads need identity and scope checks, not recent ownership evidence.

## Ownership and observation

Launch only within established authority; a brief-only request does not authorize a launch. A delegated launcher owns one launch, not delivery or further handoffs.

Before dispatch, assign one owner and record the assignment, owner, and launch ID in the [project record](../../../templates/project.md). Keep native thread and terminal IDs distinct. Record launch, grouping, startup, and delivery evidence separately; leave unobserved startup unconfirmed. Silence or queued messages prove neither success nor failure.

Uncertain launches may already be running: preserve the prompt and reconcile before retrying. Correlation IDs do not deduplicate. Repair only the failed part of a partially accepted launch.

Transfer only after the former writer stops and a named successor accepts the remaining obligations; record that acceptance and unfinished work before the successor writes. Returning coordination to the lead does not transfer execution ownership. Idle sessions retain their assignments.

Executors use [monitor](../../monitor/SKILL.md) for repeated dependency observation. Leads do not launch a second watcher for the same dependency or request milestone reports.

## Current-state records

Keep session bookkeeping in one local project record, separate from the external issue or project. Update it when ownership, prerequisites, acceptance, or the next action changes; avoid duplicating updates across briefs and records. Distinguish the delivery endpoint from its next milestone, retain pending gates and resumption triggers, and replace stale state in place.

Linear and other external trackers are not session coordination logs. Add narrative updates only for consequential decisions that future work needs, with the reason and affected scope; update authorized issue fields when actual project state changes. Keep launch IDs, acknowledgements, progress, waits, watcher output, and retirement details local. Tracker-maintenance authority does not require a post for each event. The lead records a shared decision once on the relevant issue; executors do not mirror it across tickets.

## Delivery state and blockers

Executors work independently, maintain delivery artifacts and authorized ticket state, and leave acceptance evidence with those artifacts. No completion report or acknowledgement to the lead is required.

Shared files or nearby work alone do not require coordination. Inspect available code, diffs, PRs, and assignment records; use isolated worktrees and resolve merge conflicts during integration. Do not ask other sessions to confirm prospective edits or file ownership. Contact another execution session only when blocked and unable to proceed without its action, naming the blocked operation and specific action needed; normally bring that blocker to the lead. Continue work that does not depend on the reply.

When resuming or deciding which work is ready, the lead refreshes the linked tickets, PRs, and acceptance evidence. Assess those sources against the assigned finish line: a Done ticket or merged PR establishes completion only when it satisfies that endpoint. Use a linked local artifact for evidence that has no external home. Do not require a message to accept completed work or unblock a dependency, poll owners for status, or duplicate executor-owned watches.

Executors present concrete merge or approval requests directly to the user and bring blockers needing an unavailable decision, authority, or outside help to the user first. A ready PR, unavailable permission, or completed set of available checks does not end ownership when acceptance remains open. Leads contact active owners only to resolve a blocker or convey a necessary change to or cancellation of the assignment.

Use permitted native messaging for blockers. If unavailable, raise the blocker to the user; do not use a tracker as a fallback message bus. Silence alone is not a reason to contact or replace an owner.

## Launch interface

Honor the requested or established launch interface and use its installed integration. Otherwise, prefer available native session capabilities. Supply the assignment and retain returned identifiers in the project record. If the selected interface is unavailable, resolve the choice before launching a substitute.

Include any requested title in the brief and pass it at creation when supported. Terminal and native session titles are separate; have the receiver set a requested native title before work and record unavailable title controls locally.

## Retirement

The lead owns retirement after verifying the delivery's acceptance criteria, cancellation of the assignment, or an accepted transfer to a named successor. An intermediate milestone or pending user gate is insufficient. Preserve the outcome, evidence, and any accepted successor obligations in the project record first; confirm no active descendants or unfinished work depend on the session. Verified acceptance does not itself grant cleanup authority.

Within established cleanup authority, close the execution session through the selected interface and its installed integration. Verify the recorded identity and preserve unrelated work sharing its resources. Let the integration own closure mechanics, confirmation, and uncertain-result handling.

After the last execution session retires, dissolve its project group through the selected integration if only the lead's session remains and the integration supports preserving it. Keep the lead open; this is presentation cleanup, not project completion. Record the dissolved group ID as retired, retain the lead's origin and group name, and recreate the group around that origin on the next launch. Leave groups containing other sessions intact.

Record retirement evidence or the blocker and next action in the project record. If the integration is unavailable or closure is unconfirmed, leave cleanup pending. Archiving a session, closing its runtime, and deleting its worktree are separate operations with separate authority and evidence. Cleanup failure does not undo acceptance.
