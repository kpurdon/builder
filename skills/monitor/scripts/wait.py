#!/usr/bin/env python3
"""Bounded, read-only dependency polling; emit only a terminal JSON observation."""
import argparse
from datetime import datetime, timezone
import json
import math
import re
import signal
import subprocess
import time


EXIT = {"ready": 0, "failed": 1, "error": 2, "superseded": 3,
        "timeout": 4, "cancelled": 130}


def result(status, **evidence):
    return {"status": status, **evidence}


def command(argv, deadline):
    remaining = deadline - time.monotonic()
    if remaining <= 0:
        raise TimeoutError
    process = subprocess.run(argv, capture_output=True, text=True,
                             timeout=min(30, remaining), check=False)
    if process.returncode:
        # Do not forward arbitrary CLI output (which can contain credentials).
        raise ValueError(f"{argv[0]} read failed with exit {process.returncode}; owner must inspect access/target")
    return json.loads(process.stdout)


def pr_target(args, deadline, checks=False):
    fields = "headRefOid,state" + (",statusCheckRollup" if checks else "")
    return command(["gh", "pr", "view", str(args.pr), "--repo", args.repo,
                    "--json", fields], deadline)


def changed_pr(data, sha):
    if data["headRefOid"] != sha or data["state"] != "OPEN":
        return result("superseded", head=data["headRefOid"], state=data["state"])
    return None


def ci_state(checks, expected):
    selected = []
    for name in expected:
        matches = [c for c in checks if c.get("name", c.get("context")) == name]
        if len(matches) > 1:
            raise ValueError(f"ambiguous check name: {name}")
        if not matches:
            selected.append({"name": name, "state": "missing"})
            continue
        check = matches[0]
        if "conclusion" in check:
            state = check.get("conclusion") if check.get("status") == "COMPLETED" else "PENDING"
        else:
            state = check["state"]
        selected.append({"name": name, "state": state,
                         "url": check.get("detailsUrl", check.get("targetUrl"))})
    states = {c["state"] for c in selected}
    failures = {"FAILURE", "ERROR", "CANCELLED", "TIMED_OUT", "ACTION_REQUIRED", "STARTUP_FAILURE", "STALE"}
    successes = {"SUCCESS", "NEUTRAL", "SKIPPED"}
    pending = {"PENDING", "EXPECTED", "missing"}
    if states - failures - successes - pending:
        raise ValueError("unknown check state; owner interpretation required")
    status = "failed" if states & failures else "pending" if states & pending else "ready"
    return result(status, checks=selected)


def review_state(reviews, sha, reviewer, after=None):
    matches = [r for r in reviews if r.get("commit_id") == sha
               and r.get("user", {}).get("login", "").casefold() == reviewer.casefold()
               and r.get("state") in {"APPROVED", "CHANGES_REQUESTED", "COMMENTED"}
               and r.get("submitted_at")
               and (after is None or timestamp(r["submitted_at"]) > after)]
    if not matches:
        return result("pending", reviewer=reviewer)
    latest = max(matches, key=lambda r: timestamp(r["submitted_at"]))
    return result("ready", review={key: latest[key] for key in
                                   ["id", "state", "commit_id", "submitted_at", "html_url"]})


def github(args, deadline):
    data = pr_target(args, deadline, checks=args.action == "ci")
    changed = changed_pr(data, args.sha)
    if changed:
        return changed
    if args.action == "ci":
        observation = ci_state(data.get("statusCheckRollup") or [], args.check)
    else:
        pages = command(["gh", "api", f"repos/{args.repo}/pulls/{args.pr}/reviews",
                         "--paginate", "--slurp"], deadline)
        observation = review_state([r for page in pages for r in page],
                                   args.sha, args.reviewer, args.after)
    if observation["status"] != "pending":
        return changed_pr(pr_target(args, deadline), args.sha) or observation
    return observation


class Rollout:
    def __init__(self, expected, revision_source, revision_key, revision_value):
        self.expected = expected
        self.revision_source = revision_source
        self.revision_key = revision_key
        self.revision_value = revision_value
        self.uid = None
        self.initial = None
        self.seen_target = False

    def observe(self, deployment):
        meta, spec = deployment["metadata"], deployment["spec"]
        status = deployment.get("status", {})
        images = {c["name"]: c["image"] for c in spec["template"]["spec"]["containers"]}
        revision = spec["template"].get("metadata", {}).get(self.revision_source, {}).get(self.revision_key)
        identity = (images, revision)
        if self.uid is None:
            self.uid, self.initial = meta["uid"], identity
        evidence = {"uid": meta["uid"], "generation": meta["generation"],
                    "observed_generation": status.get("observedGeneration"), "images": images,
                    "revision": {"source": self.revision_source, "key": self.revision_key, "value": revision},
                    "replicas": {k: status.get(k, 0) for k in
                                 ["replicas", "updatedReplicas", "readyReplicas", "availableReplicas"]},
                    "desired": spec.get("replicas", 1)}
        if meta["uid"] != self.uid or meta.get("deletionTimestamp"):
            return result("superseded", **evidence)
        if images != self.expected or revision != self.revision_value:
            state = "superseded" if self.seen_target or identity != self.initial else "pending"
            return result(state, **evidence)
        self.seen_target = True
        if status.get("observedGeneration", 0) < meta["generation"]:
            return result("pending", **evidence)
        if any(c.get("type") == "Progressing" and c.get("status") == "False"
               and c.get("reason") == "ProgressDeadlineExceeded"
               for c in status.get("conditions", [])):
            return result("failed", **evidence)
        desired = evidence["desired"]
        ready = desired > 0 and all(n == desired for n in evidence["replicas"].values())
        return result("ready" if ready else "pending", **evidence)


def wait(probe, timeout, interval, clock=time.monotonic, sleep=time.sleep):
    deadline = clock() + timeout
    last = None
    try:
        while clock() < deadline:
            last = probe(deadline)
            if clock() >= deadline:
                break
            if last["status"] != "pending":
                return last
            sleep(min(interval, max(0, deadline - clock())))
    except (TimeoutError, subprocess.TimeoutExpired):
        if clock() < deadline:
            return result("error", reason="observation command exceeded its 30-second limit", last=last)
    except KeyboardInterrupt:
        return result("cancelled", last=last)
    except (ValueError, KeyError, TypeError, OSError) as exc:
        return result("error", reason=str(exc), last=last)
    return result("timeout", last=last)


def positive(value):
    number = float(value)
    if not math.isfinite(number) or number <= 0:
        raise argparse.ArgumentTypeError("must be positive and finite")
    return number


def timestamp(value):
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("timestamp must include a timezone")
    return parsed


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    actions = parser.add_subparsers(dest="action", required=True)
    for action in ["ci", "review", "rollout"]:
        sub = actions.add_parser(action)
        sub.add_argument("--timeout", type=positive, required=True)
        sub.add_argument("--interval", type=positive, default=30)
        if action in {"ci", "review"}:
            sub.add_argument("--repo", required=True)
            sub.add_argument("--pr", required=True, type=int)
            sub.add_argument("--sha", required=True)
        if action == "ci":
            sub.add_argument("--check", action="append", required=True)
        elif action == "review":
            sub.add_argument("--reviewer", required=True)
            sub.add_argument("--after", type=timestamp)
        else:
            for flag in ["context", "namespace", "deployment"]:
                sub.add_argument("--" + flag, required=True)
            sub.add_argument("--image", action="append", required=True)
            revision = sub.add_mutually_exclusive_group(required=True)
            revision.add_argument("--revision-label", metavar="KEY=VALUE")
            revision.add_argument("--revision-annotation", metavar="KEY=VALUE")
    args = parser.parse_args()
    if args.action in {"ci", "review"}:
        if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", args.repo) or args.pr < 1:
            parser.error("use OWNER/REPO and a positive PR number")
        if not re.fullmatch(r"[0-9a-f]{40}", args.sha):
            parser.error("--sha must be the full lowercase commit SHA")
    else:
        images = {}
        for value in args.image:
            name, sep, image = value.partition("=")
            if not sep or not name or not image or name in images:
                parser.error("use unique --image CONTAINER=EXACT_IMAGE values")
            images[name] = image
        args.image = images
        args.revision_source = "labels" if args.revision_label else "annotations"
        key, sep, value = (args.revision_label or args.revision_annotation).partition("=")
        if not sep or not key or not value:
            parser.error("use a pod-template revision KEY=VALUE")
        args.revision_key, args.revision_value = key, value
    return args


def main():
    args = parse_args()
    def cancel(*_):
        raise KeyboardInterrupt
    signal.signal(signal.SIGTERM, cancel)
    if args.action == "rollout":
        watcher = Rollout(args.image, args.revision_source, args.revision_key, args.revision_value)
        def probe(deadline):
            deployment = command(["kubectl", "--context", args.context, "--namespace", args.namespace,
                                  "get", "deployment", args.deployment, "-o", "json"], deadline)
            return watcher.observe(deployment)
        target = {k: getattr(args, k) for k in ["context", "namespace", "deployment", "image",
                                                             "revision_source", "revision_key", "revision_value"]}
    else:
        def probe(deadline):
            return github(args, deadline)
        target = {k: getattr(args, k) for k in ["repo", "pr", "sha"]}
    observation = wait(probe, args.timeout, args.interval)
    observation.update(action=args.action, target=target, observed_at=datetime.now(timezone.utc).isoformat())
    print(json.dumps(observation), flush=True)
    return EXIT[observation["status"]]


if __name__ == "__main__":
    raise SystemExit(main())
