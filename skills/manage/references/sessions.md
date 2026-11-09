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

## Current-state records

At handoff or a material state change, update owners, prerequisites, decisions, and next actions in the assignment and project record. Distinguish the delivery endpoint from its next milestone; record pending gates and resumption triggers. Replace stale instructions in place, link history separately, and mark unverified state.

## Completion reporting

Executors report completion to the return destination with assignment, launch, and thread IDs; the outcome reached; artifacts or revision; and acceptance evidence. Label intermediate results as milestones or waits, with the retained owner and next action. Send event-driven milestones when they unblock dependent work; leads do not poll for status or require startup acknowledgements, routine progress reports, or intermediate approvals.

Executors present concrete merge or approval requests directly to the user and bring blockers needing an unavailable decision, authority, or outside help to the user first. Involve the lead for a concrete dependency between assignments, naming the needed action. A ready PR, unavailable permission, or completed set of available checks does not end ownership when acceptance remains open. Leads may relay material scope changes without repeatedly prompting active owners.

Use permitted native messaging or the authorized governing record. If neither is available, keep the report in the executor's final response and disclose that it could not be delivered. Reconcile on concrete failure evidence; silence alone is insufficient.

## Launch interface

Honor the requested or established launch interface and use its installed integration. Otherwise, prefer available native session capabilities. Supply the assignment and retain returned identifiers in the project record. If the selected interface is unavailable, resolve the choice before launching a substitute.

Include any requested title in the brief and pass it at creation when supported. Terminal and native session titles are separate; have the receiver set a requested native title before work and report unavailable title controls at completion.

## Retirement

The lead owns retirement after verifying the delivery's acceptance criteria, cancellation of the assignment, or an accepted transfer to a named successor. A milestone report, user gate, or handback to the PM is insufficient. Preserve the outcome, evidence, and any accepted successor obligations in the project record first; confirm no active descendants or unfinished work depend on the session. A completion report alone does not establish acceptance or cleanup authority.

Within established cleanup authority, close the execution session through the selected interface and its installed integration. Verify the recorded identity and preserve unrelated work sharing its resources. Let the integration own closure mechanics, confirmation, and uncertain-result handling.

Record retirement evidence or the blocker and next action in the project record. If the integration is unavailable or closure is unconfirmed, leave cleanup pending. Archiving a session, closing its runtime, and deleting its worktree are separate operations with separate authority and evidence. Cleanup failure does not undo acceptance.
