# Wait helpers

For rollout assignments, select the configured delivery integration first; see [Akuity MCP](akuity.md). The `rollout` command below is a direct Kubernetes Deployment adapter, not the watcher's general workload support boundary.

Run `python3 <monitor-skill>/scripts/wait.py <action> ...` from the assigned working directory. Requires Python 3.10+, plus authenticated `gh` for GitHub or `kubectl` for Kubernetes. Helpers perform reads only and keep polling outside the model. They emit one terminal JSON record. `--timeout` is a required number of seconds; `--interval` defaults to 30 seconds. Each external command is bounded by the remaining deadline and at most 30 seconds. Cancel with SIGINT or SIGTERM; do not abandon a running helper.

| Action | Required target and criteria | Evidence returned |
| --- | --- | --- |
| `ci` | `--repo OWNER/REPO --pr NUMBER --sha FULL_SHA --check NAME` (repeat for every expected check) | Selected check states and links for that head. Success, neutral, and skipped count as complete; use different acceptance evidence if a check must actually run. Missing checks stay pending; duplicate names or unknown states require owner interpretation. |
| `review` | `--repo OWNER/REPO --pr NUMBER --sha FULL_SHA --reviewer LOGIN` | A submitted PR review by that exact account on that commit, including state and URL. Optional `--after ISO_TIMESTAMP` excludes earlier submissions. This detects arrival, including changes requested; the owner assesses the findings. |
| `rollout` | `--context CONTEXT --namespace NAMESPACE --deployment NAME --image CONTAINER=EXACT_IMAGE` (repeat for every regular container) | Deployment UID, template revision, generation, image identities, and replica counts. Use immutable digests, or an immutable-tag guarantee established by the owner. |

Examples (replace all targets with the assignment's values):

```sh
python3 /path/to/monitor/scripts/wait.py ci --repo owner/repo --pr 42 --sha FULL_SHA --check unit --check integration --timeout 1800
python3 /path/to/monitor/scripts/wait.py review --repo owner/repo --pr 42 --sha FULL_SHA --reviewer reviewer-login --timeout 1800
python3 /path/to/monitor/scripts/wait.py rollout --context staging --namespace app --deployment api --image api=registry/api@sha256:DIGEST --revision-label app.kubernetes.io/version=REVISION --timeout 1800
```

Statuses: `ready` (exit 0), `failed` (1), `error` (2), `superseded` (3), `timeout` (4), `cancelled` (130). A timeout includes the last observation. Reconfirm the PR head before returning a terminal CI or review result; a changed head or closed PR ends the watch. GitHub review comments without a commit-associated submitted review are unsupported: return that limitation to the owner rather than infer approval from a comment or green check.

The owner must identify the target with a pod-template label or annotation that changes for the intended release, including configuration-only changes. An image or app-version label that remains unchanged across the intended config update is insufficient; use a config checksum or another release identifier. If no such identifier exists, escalate for another observation method.

Rollout monitoring waits through the initial old template. If its images or selected revision change to an unexpected template, the Deployment is recreated, or the expected template is subsequently replaced, report `superseded`. Success requires the complete regular-container image map, expected template revision, observed generation, a nonzero desired replica count, and total/updated/ready/available counts all matching desired replicas. Init containers, pod image IDs, other workload kinds, Kargo promotion policy, and application behavior need separate acceptance evidence. Capture each workload separately when an assignment has several targets; one workload becoming ready does not establish environment-wide readiness.

The helper owns no durable scheduler. Native subagent completion supplies the return path while the host is running; session shutdown, process loss, and future automatic resumption must be handled by the delivery owner.
