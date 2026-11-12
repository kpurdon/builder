# Quality and evidence

## Linking sources and evidence

Link consequential claims to inspectable original sources with enough context to reproduce and interpret them. Summaries and landing pages do not substitute for evidence. Disclose missing sources or access; retain original captures when live data cannot be revisited.

## Presenting validation evidence

Prefer the running application or branch preview for UI validation. Check its backend compatibility and exercise the behavior it supports; use component fixtures to cover cases it cannot exercise.

Choose screenshots, recordings, queries, or logs that demonstrate the claim. Preserve context and disclose edits and limitations that affect interpretation. Use recordings or behavioral checks for interactions a screenshot cannot prove; screenshots alone cannot prove backend correctness.

For visible changes:

- Compare labeled base/head captures with matching scenario, data, viewport, and interaction state. Disclose missing baselines or material differences.
- Show a readable region with enough context to interpret it and link originals. Link full-size images when compact captures are unavailable.
- Identify each capture's environment and revision, and label synthetic fixtures.

For PRs, use the [description guidance](../skills/execute/references/pr-description.md) to select and place evidence. Keep captures outside tracked source and verify published artifacts. Reconcile partial upload success before retrying.

## Operational evidence

Distinguish source, CI, deployment, runtime acceptance, and customer exposure. Test the intended artifact and affected behavior, not just command or pod health. Make impact comparisons reproducible; samples are not population counts, and absent errors with inadequate telemetry do not establish health.
