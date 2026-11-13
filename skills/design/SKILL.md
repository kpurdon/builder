---
name: design
description: Clarify engineering problems, resolve design choices, and plan delivery.
---

# design

Follow the [working agreement](../../references/working-agreement.md).

Clarify the problem and investigate unknowns that could change the recommendation. Compare viable approaches and explain consequential tradeoffs; recommend a design, an experiment, or stopping.

Talk through consequential choices with the user when their input is needed, then describe the agreed direction in the document. Resolve routine implementation details independently. Keep genuine unknowns explicit and recommendations distinct from accepted decisions; retain alternatives when the requested document is a comparison. Ordinary drafting needs no added approval step.

When asked for a delivery plan, build on settled decisions and reuse the governing [record](../../templates/project.md). Define testable outcomes, acceptance criteria, dependencies, and rollout order. Apply the [PR dependency criteria](../execute/references/pr-delivery.md) when choosing branch bases. Distinguish merge order from rollout dependencies. For rollout or recovery plans, use [operational procedures](../execute/references/operations.md).

Match the depth to the request and leave decisions and open questions usable by the delivery owner. Design and planning alone do not authorize implementation or session launches.
