# PR descriptions

Read the final diff against its actual base and verify consequential claims. Write for someone reviewing that diff; keep the description proportional to the change.

## Description

- Lead with a relevant existing ticket link when available, then a short paragraph explaining the problem and changed behavior. Make the explanation stand alone. Use headings only when they help organize a longer description.
- Describe the full scope: name backend/API changes and dependencies when present, even when the visible result is a frontend change. In a stack, describe this layer and link its prerequisite.
- Include implementation details, examples, tradeoffs, or dependencies only when they materially help review. Omit work history and inventories of changed layers or unchanged behavior.
- Honor explicit repository requirements; template headings alone do not make sections mandatory. Omit boilerplate sections, including Docs and Security when they add nothing relevant.

For small changes, a ticket link and one short paragraph usually suffice: “The backfill pilot hit its batch cap. Start a new Job from the saved checkpoint, remove the cap, and extend the budget from five minutes to two hours. Merging starts the continuation in staging.”

## Validation

Put screenshots and other meaningful evidence beyond routine PR checks inside one collapsed section:

```html
<details>
<summary>Validation</summary>

<br>

<!-- Labeled evidence and what it demonstrates. -->

</details>
```

When including validation evidence, use the shared [evidence guidance](../../../references/quality.md#presenting-validation-evidence). Explain what the evidence demonstrates and where it came from; mention limitations only when they affect interpretation or a review decision. For non-routine pre-merge checks, state the expected or observed result and distinguish pending from completed. Links support the explanation rather than replace it.

Omit routine test results and counts, command inventories, lint/typecheck results, CI status, and review approvals. Omit Validation when there is no meaningful evidence or non-routine pre-merge check to include. Keep delivery status in the conversation or authorized tracker updates. Post-merge validation, rollout, and other future work belong in the tracker; do not create or change tracking records without authorization.

## Final pass

On every body update, rewrite for the current diff rather than appending progress. Remove stale explanations, repeated facts, and unnecessary detail; put retained validation evidence in the collapsed section. Passing delivery gates alone is no reason to edit the body. A reviewer should quickly understand why the change exists and what it does.

For authorized publication, verify the repository, branch/base, destination, and draft state; update an existing PR when suitable. Check the published description, rendered evidence, and links.
