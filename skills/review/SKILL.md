---
name: review
description: Assess changes, verify review findings, and identify material gaps in review coverage.
---

# review

Follow the [working agreement](../../references/working-agreement.md).

Establish the target revision or artifact, intended behavior, accepted decisions, and consequential constraints. Assess code, configuration, or guidance within the requested scope without editing or publishing feedback unless asked.

Use available native, automated, and human reviews as evidence. Check their scope and revision before relying on them; an existing independent review can satisfy that requirement. A passing check alone does not establish review coverage, and the author's assessment is not independent review. Apply repository-specific reviewer requirements and workflows from repository or personal guidance.

Verify findings against the current change and surrounding behavior. Distinguish confirmed defects, duplicates, stale findings, preferences, and unresolved questions; explain the evidence for consequential dispositions. Missing new tests or removing unnecessary instructions is not itself a finding.

Review material risks left uncovered by existing evidence, using available review capabilities when useful. Request focused follow-up when changes invalidate earlier findings or coverage; do not repeat a generic review solely because a different tool produced it. Assess PR clarity and rendered evidence when they affect understanding or support a claim, using the [PR-description guidance](../execute/references/pr-description.md).

Return actionable findings with their triggering conditions, impact, and supporting evidence, plus material coverage limits. Leave fixes and required follow-up to the [delivery owner](../execute/SKILL.md); review findings do not establish [runtime acceptance](../validate/SKILL.md).
