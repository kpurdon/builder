# CI failure evidence

Requires Python 3.10+ and an authenticated `gh` with access to the target repository and Actions logs. Run:

```sh
python3 /path/to/builder/skills/monitor/scripts/ci.py --repo owner/repo --pr 42 --sha FULL_SHA --output-dir /absolute/new/evidence-directory --timeout 120
```

The output directory must not exist. The helper performs GitHub reads only and writes a private local `packet.json` plus bounded job logs. It emits a short JSON result pointing to the packet. Defaults: at most 5 failed jobs, 2 MiB per log, and 30 seconds per command within the required total deadline. `--max-jobs` and `--max-log-bytes` change those bounds. Metadata reads are capped at 4 MiB. No polling, workflow reruns, artifact downloads, or arbitrary commands from logs.

The packet records the target SHA, initial/final PR check snapshots, failed-check source URLs, job/run IDs and attempt numbers, failed step names, log paths/digests, line-numbered error candidates, observation time, and gaps. Candidate excerpts are a bounded heuristic, not root-cause findings or a complete test report. The watcher can inspect more of the captured local log. Logs may contain repository data; keep them local unless sharing is explicitly requested.

GitHub.com Actions job links are supported. Unsupported providers/URLs, inaccessible or expired logs, in-progress jobs, limits, unknown metadata, or truncated logs produce `partial` with specific gaps. A head change, changed failed-check snapshot, or rerun detected during collection produces `superseded`; preserve historical artifacts but do not use them as current-head proof. Job/run revision and attempt must match before logs are accepted. Workflows using a different merge revision require owner interpretation, not implicit equivalence to the requested SHA.

Statuses: `complete` (exit 0), `no_failures` (0), `partial` (1), `superseded` (3), `error` (2), `cancelled` (130). `complete` means the observed failed checks were collected within the limits; it does not mean CI passed. `no_failures` can coexist with pending or absent checks. Access, deadline, and metadata failures remain visible, including when final freshness checks could not run.
