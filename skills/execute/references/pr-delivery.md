# PR delivery

Default to ready for the user's merge decision only when the user's request, governing acceptance criteria, and repository policy leave delivery completion unspecified. They may require a reviewed draft or work beyond merge; a manager's PR milestone does not replace that endpoint.

Stack a PR only when it requires an unmerged contract or behavior from its parent; name that dependency before choosing the base. Shared files, project membership, execution order, and avoiding edit conflicts do not establish a dependency. Base independently shippable changes on trunk in isolated worktrees; apply the [session blocker guidance](../../manage/references/sessions.md#delivery-state-and-blockers) when another owner's action is required. Reassess dependencies when splitting or restructuring existing work.

Separate backend/API changes and frontend changes that consume them into stacked PRs, backend first. Plan the layers before implementation and use the host's stack tooling for mechanics. Keep the backend compatible with the existing frontend; merge order alone does not establish backend availability for frontend validation.

1. Create or update the PR using the [description guidance](pr-description.md), initially draft; preserve existing ready state.
2. Require independent review with no unresolved blocking findings before marking ready. Reuse existing review evidence when its scope and revision fit.
3. Await required CI and repository-required approvals for the latest head; read findings and replies across revisions. Passing checks do not replace required review approval.
4. Leave merging to the user unless explicitly authorized.

Fix confirmed problems, validate, independently re-review affected behavior, and refresh evidence. Resolve unavailable required reviews or empty CI through task or repository policy; required missing evidence blocks completion. Continue through any assigned rollout and validation.
