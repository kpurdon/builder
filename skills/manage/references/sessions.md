# Session operations

For assigned projects, apply the [project management execution boundary](../SKILL.md). Otherwise, keep short or coupled work local; separate sessions need ready assignments and a benefit exceeding coordination cost. Prefer bounded subagents for supporting contributions.

Prepare handoffs with the [brief](../../../templates/handoff.md), linking artifacts rather than transcripts. Use the [selected launch interface](#launch-interface) for authorized launches.

## Receiver selection

Use fresh sessions for new handoffs unless the user selects an existing thread. Otherwise, continue only a verified current owner; matching titles or idle status are insufficient. User-selected threads need identity and scope checks, not recent ownership evidence.

## Ownership and observation

Launch only within established authority; a brief-only request does not authorize a launch. A delegated launcher owns one launch, not delivery or further handoffs.

Before dispatch, assign one owner and record the assignment, owner, and launch ID in the [project record](../../../templates/project.md). Keep native thread and terminal IDs distinct. Record launch, grouping, startup, and delivery evidence separately; leave unobserved startup unconfirmed. Silence or queued messages prove neither success nor failure.

Uncertain launches may already be running: preserve the prompt and reconcile before retrying. Correlation IDs do not deduplicate. Repair only the failed part of a partially accepted launch.

Transfer only after the former writer stops; record the successor and unfinished work before it writes. An idle lead does not transfer or retire an executor's assignment.

## Current-state records

At handoff or a material state change, update owners, prerequisites, decisions, and next actions in the assignment and project record. Replace stale instructions in place, link history separately, and mark unverified state.

## Completion reporting

Executors report completion to the return destination with assignment, launch, and thread IDs; the outcome reached; artifacts or revision; and acceptance evidence. Reports to the lead cover completion or the escalations below. Leads do not poll for status or require startup acknowledgements, progress reports, or intermediate approvals.

Bring blockers needing an unavailable decision, authority, or outside help to the user first. Involve the lead for a concrete dependency between assignments, naming the needed action. Executors retain delivery ownership and CI, review, and deployment waits. Leads may relay material scope changes without repeatedly prompting active owners.

Use permitted native messaging or the authorized governing record. If neither is available, keep the report in the executor's final response and disclose that it could not be delivered. Reconcile on concrete failure evidence; silence alone is insufficient.

## Launch interface

Honor the requested or established launch interface and use its installed integration. Otherwise, prefer available native session capabilities. Supply the assignment and retain returned identifiers in the project record. If the selected interface is unavailable, resolve the choice before launching a substitute.

Include any requested title in the brief and pass it at creation when supported. Terminal and native session titles are separate; have the receiver set a requested native title before work and report unavailable title controls at completion.

## Retirement

The lead owns retirement after accepting a completion report or recording a transfer. Preserve the outcome and evidence in the project record first; confirm no active descendants or unfinished work depend on the session. A completion report alone does not establish acceptance or authority to close its terminal.

Within established cleanup authority, close the execution tab through the selected integration. For iTerm2, use the installed `iterm2` plugin's `tabs` skill. Match the recorded tab ID to fresh inventory and check every pane, including minimized panes; keep tabs with unrelated or unfinished work open. Follow the integration's confirmation and uncertain-result handling; closure authority alone does not authorize force-closing.

Record tab closure evidence or the blocker and next action in the project record. If the integration is unavailable or closure is unconfirmed, leave cleanup pending. Archiving, closing tabs, and deleting worktrees are separate operations with separate authority and evidence. Cleanup failure does not undo acceptance.
