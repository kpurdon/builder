---
name: execute
description: Deliver accepted engineering changes, interventions, or artifacts.
---

# execute

Follow the [working agreement](../../references/working-agreement.md).

Own the accepted outcome through delivery and validation by default. Determine and record its finish line and required evidence from the user's request, governing acceptance criteria, and repository policy. An explicit report-only assignment or policy-defined reviewed draft can be the endpoint; a handoff brief must not silently narrow a broader delivery to PR readiness or available checks. Use the [PR default](references/pr-delivery.md) only when those sources leave PR delivery unspecified. Resolve consequential ambiguity; handle routine steps independently. Required gates do not grant merge or deployment authority.

Begin with investigation or design when needed, then continue through authorized implementation in the same session. Own the work and waits through completion, including applicable review, fixes, CI, authorized rollout, and validation. Retain ownership while awaiting a user gate or dependency, recording the next action and resumption trigger. Use independent review for non-PR work when required or warranted by its consequences.

For PR descriptions and reviewer handoffs, use the [description guidance](references/pr-description.md). A description-only request ends with draft text unless publication is requested.

For handoff briefs, use [session operations](../manage/references/sessions.md). For delegated work, follow its [completion reporting contract](../manage/references/sessions.md#completion-reporting).

For interventions, rollout, recovery, or operational artifacts, use [operational procedures](references/operations.md). For Datadog work, use [Datadog guidance](../investigate/references/datadog.md). Investigate unexpected results.
