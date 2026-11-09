# Akuity rollout observation

Use the existing authenticated Akuity MCP connection when it is the user's configured rollout interface. Discover the tools and their current input schemas in the worker's client; server prefixes and available tools vary by endpoint and permissions. The watcher reports authentication failures to the owner, who handles [login refresh](#login-refresh) before resuming observation. Do not build a separate API client or install a connection as part of a watch. Missing access is an explicit readiness gap, not a reason to silently switch to pod polling.

## Login refresh

During authorized work, the delivery owner may refresh authentication for the existing server and account without asking for additional permission: `codex mcp login <configured-server-name>` for MCP, or `kargo login https://<kargo-host> --sso` for the CLI. A bare `kargo login` can reuse a previously saved server and method after confirming they match the assignment. This permits normal login and token refresh, not changing accounts, granting broader scopes, or creating new connections. If browser SSO or MFA needs the user, launch the flow and explain the required interaction; do not treat it as another permission request.

MCP and CLI credentials are separate. Verify a successful login with a scoped read through the interface being used, then resume the same target within its remaining deadline. Do not repeatedly retry a rejected login without a concrete correction. If login remains blocked or the deadline expires, report the blocker or timeout instead of implying that observation is continuing.

For a platform `user not found` error, distinguish Akuity Platform identity from direct instance SSO before assuming credentials are expired. The [direct Kargo endpoint](https://docs.akuity.io/kargo/managing-instances/settings/security-and-access/mcp-access/) is `https://<kargo-host>/mcp` and uses that instance's identity and RBAC. It does not establish Argo CD access. Dex requires a `localhost` callback rather than `127.0.0.1`; use the connection's registered client and matching callback URL/listener port under [Codex OAuth settings](https://learn.chatgpt.com/docs/extend/mcp). Endpoint or callback setup is a separate repair from routine login.

Check CLI/server compatibility when login fails before SSO. Kargo v1.12 removed the legacy API used by old CLIs; an HTTP 405 from an old client can be a version mismatch rather than an authentication failure. Use a compatible CLI and consult the [release guidance](https://docs.kargo.io/release-notes/v1.12.0), rather than repeatedly logging in.

## Assignment and evidence

The owner supplies the instance, project/stage or Argo CD application, environment, immutable target artifact/revision, and the exact gate to observe. Carry the mapping between source commit, freight, GitOps revision, and workload image where those identities differ. A source SHA cannot be assumed to equal the application's sync revision. Pin a promotion ID when waiting for a particular promotion attempt. If a name such as Shipit denotes a local delivery flow, resolve it to its existing Kargo/Argo resources; do not invent a Shipit MCP operation.

Use the smallest set of reads that establishes the assigned gate. Typical tools in the [Akuity tool reference](https://docs.akuity.io/akuity-portal/agentic-control-plane/mcp-server/tool-reference/) are:

| Gate | Candidate reads | Completion evidence |
| --- | --- | --- |
| Promotion attempt | `get_kargo_promotion`, `get_kargo_freight` | Exact promotion, stage, and freight artifacts match the assignment; that attempt succeeded. |
| Stage arrival | `get_kargo_stage`, `get_kargo_freight` | The stage's current freight resolves to the intended artifacts and satisfies the assigned health/verification criteria. |
| Application/workload readiness | `get_argocd_application`, `get_argocd_application_tree` | Expected desired and applied revision(s), sync/health, and the named workload's state satisfy the assigned criteria. An Argo Rollout is identified by its group, kind, namespace, and name in that application's resource tree. |

Promotion success does not establish workload readiness. A healthy application or resource alone does not prove that the intended release is running. For multiple sources or workloads, account for every assigned target. Preserve the distinction between Argo CD application health and the workload's own rollout state. If MCP responses lack required live revision, image, replica, or rollout-condition evidence, report the missing fields to the owner; do not call the gate ready or substitute a weaker pod-readiness check. An independently justified read-only fallback must retain the same target and criteria and be disclosed by the owner.

## Bounded watch

The published tools provide snapshots rather than a dedicated wait operation. Use native waits between scoped reads, normally at least 30 seconds apart, within the owner's finite deadline. Do discovery once; avoid repeated fleet listings or log dumps. Bound individual calls by the remaining deadline where the client supports it. If the client cannot bound or resume an in-flight call, disclose that limitation; a deadline is not guaranteed cancellation. Check time before each call/wait and stop when it expires.

Initial older state may remain pending while the intended release arrives. Record that baseline. A competing promotion or release that replaces the assigned attempt/target is `superseded`; do not follow the newest release automatically. Unknown states or ambiguous artifact mappings require owner interpretation. Before returning `ready`, reconfirm the target identity and relevant terminal state to catch a replacement during observation.

Return `ready`, `failed`, `error`, `superseded`, `timeout`, or `cancelled`, with observation time, resource identities/links, matched artifact/revision, relevant state, and the next action. Include the last observation on timeout. Unavailable tools, authentication failures, or insufficient evidence are `error`. Report a paused rollout or approval gate to the owner as an actionable blocker rather than approving or resuming it. Observe only: do not refresh or sync an Argo CD application, promote or retry a deployment, patch or restart workloads, or launch an Akuity AI Agent. Runtime and UI acceptance remain with the delivery owner.
