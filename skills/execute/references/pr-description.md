# PR descriptions

Read the final diff against its actual base and verify consequential claims. Apply the shared [quality and evidence standards](../../../references/quality.md).

## Description

- Lead with a relevant existing ticket link when available, then a short paragraph explaining the problem and changed behavior. Make the explanation stand alone. Use headings only when they help organize a longer description.
- Include implementation details, examples, tradeoffs, or dependencies only when they materially help review. Omit work history and inventories of changed layers or unchanged behavior.
- Honor explicit repository requirements; template headings alone do not make sections mandatory. Omit boilerplate sections, including Docs and Security when they add nothing relevant.

## Validation

Put screenshots and other meaningful evidence beyond routine PR checks inside one collapsed section:

```html
<details>
<summary>Validation</summary>

<br>

<!-- Labeled evidence and what it demonstrates. -->

</details>
```

Use the shared [visual evidence guidance](../../../references/quality.md#presenting-validation-evidence) for captures. Explain what the evidence demonstrates and where it came from; mention limitations only when they affect interpretation or a review decision. For non-routine pre-merge checks, state the expected or observed result and distinguish pending from completed. Links support the explanation rather than replace it.

Omit routine test results and counts, command inventories, lint/typecheck results, and CI status. Omit Validation when there is no meaningful evidence or non-routine pre-merge check to include. Post-merge validation, rollout, and other future work belong in the tracker; do not create or change tracking records without authorization.

## Final pass

Rewrite for the final diff before publishing. Remove stale explanations, repeated facts, and unnecessary detail. A reviewer should quickly understand why the change exists and what it does.

For authorized publication, verify the repository, branch/base, destination, and draft state; update an existing PR when suitable. Check the published description, rendered evidence, and links.
