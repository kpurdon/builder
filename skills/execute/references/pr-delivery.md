# PR delivery

Default to ready for the user's merge decision only when the user's request, governing acceptance criteria, and repository policy leave [delivery completion](../SKILL.md) unspecified. They may require a reviewed draft or work beyond merge; a manager's PR milestone does not replace that endpoint.

1. Create or update the PR using the [description guidance](pr-description.md), initially draft; preserve existing ready state.
2. Require independent [review](../../review/SKILL.md) with no unresolved blocking findings before marking ready. Reuse existing review evidence when its scope and revision fit.
3. Await required CI and repository-required approvals for the latest head; read findings and replies across revisions. Passing checks do not replace required review approval.
4. Leave merging to the user unless explicitly authorized.

Fix confirmed problems, validate, independently re-review affected behavior, and refresh evidence. Resolve unavailable required reviews or empty CI through task or repository policy; required missing evidence blocks completion. Continue through any assigned rollout and validation.
