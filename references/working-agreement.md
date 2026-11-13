# Shared working agreement

Use judgment to reach the agreed outcome; switch skills without unnecessary phases or handoffs. Keep remaining work and ownership explicit.

For substantial designs, investigations, and plans, default to reviewing the result with the user incrementally in conversation. Begin the walkthrough when the work is ready; do not stop at a file link or an offer to explain later. Start with the concrete problem and its consequence, then cover one coherent finding or consequential choice per turn, with the evidence, tradeoffs, and recommendation needed to assess it. Wait for the user's questions, acceptance, or decision before advancing the walkthrough, and carry decisions and open questions forward. Continue authorized work that does not depend on a pending user decision. Artifacts support the discussion. Follow explicit requests for a full report or summary instead.

Use short, connected paragraphs and remove repeated caveats. Keep scope diagrams focused on the main flow and responsibilities, with simple labels; put implementation detail in supporting engineering material where needed.

Start or reuse a Goal for substantial work under the user's applicable standing or task-specific Goal request. Activate it before substantive work using the [Goal procedure](codex.md#goals); do not wait for the user to enable it manually.

When ending a work turn, including a handoff or wait, give the user a concise, self-contained summary of the current outcome and any action needed from them, or say none is needed. Repeat relevant direct links to PRs, issues, and artifacts even when shared earlier, identifying each PR's purpose and state. Put this information before supporting detail; natural prose or short bullets are both suitable. When work remains, name its owner, next action, and any resumption trigger, making clear whether work is active or awaiting resumption. Distinguish delivery stages and unverified outcomes using the evidence guidance below.

Run required checks; add tests or documentation for concrete uncovered needs. Reassess affected evidence after fixes. Keep user configuration and runtime state outside builder.

During authorized work, the owner may reauthenticate configured MCP connections and CLIs for the existing account and scopes without renewed permission. Launch the normal login flow when needed; request user interaction only for sign-in or MFA steps that cannot be completed automatically. Verify recovery with a scoped read through the affected interface. This does not authorize changing accounts, broadening scopes, or creating connections.

Use [evidence guidance](quality.md) when gathering, evaluating, or presenting findings or validation and acceptance evidence. For PR delivery, use [PR delivery guidance](../skills/execute/references/pr-delivery.md). For iterative execution, project management, or work with Goals, sessions, or worktrees, use [Codex controls](codex.md).
