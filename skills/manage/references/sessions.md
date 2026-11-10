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

## Completion reporting

Work independently within the assignment. Report completion once to the return destination with the outcome, artifacts or revision, and acceptance evidence. Before completion, contact another execution session only when blocked and unable to proceed without its action; normally bring the blocker and needed action to the lead. Routine progress, dependency availability, and milestones do not need messages. Leads do not poll owners, require acknowledgements or intermediate approvals, or relay updates between executors.

Executors present concrete merge or approval requests directly to the user and bring blockers needing an unavailable decision, authority, or outside help to the user first. A ready PR, unavailable permission, or completed set of available checks does not end ownership when acceptance remains open. Leads contact active owners only to resolve a blocker or convey a necessary change to or cancellation of the assignment.

Use permitted native messaging for session reports. If unavailable, keep the report in the executor's final response and disclose that it could not be delivered; do not use a tracker as a fallback message bus. Reconcile on concrete failure evidence; silence alone is insufficient.

## Launch interface

Honor the requested or established launch interface and use its installed integration. Otherwise, prefer available native session capabilities. Supply the assignment and retain returned identifiers in the project record. If the selected interface is unavailable, resolve the choice before launching a substitute.

Include any requested title in the brief and pass it at creation when supported. Terminal and native session titles are separate; have the receiver set a requested native title before work and report unavailable title controls at completion.

## Retirement

The lead owns retirement after verifying the delivery's acceptance criteria, cancellation of the assignment, or an accepted transfer to a named successor. A milestone report, user gate, or handback to the PM is insufficient. Preserve the outcome, evidence, and any accepted successor obligations in the project record first; confirm no active descendants or unfinished work depend on the session. A completion report alone does not establish acceptance or cleanup authority.

Within established cleanup authority, close the execution session through the selected interface and its installed integration. Verify the recorded identity and preserve unrelated work sharing its resources. Let the integration own closure mechanics, confirmation, and uncertain-result handling.

Record retirement evidence or the blocker and next action in the project record. If the integration is unavailable or closure is unconfirmed, leave cleanup pending. Archiving a session, closing its runtime, and deleting its worktree are separate operations with separate authority and evidence. Cleanup failure does not undo acceptance.
