#!/usr/bin/env python3
"""Collect bounded, revision-pinned CI failure evidence without diagnosing or fixing it."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import re
import selectors
import signal
import subprocess
import time
from urllib.parse import urlparse

FAILURES = {'FAILURE', 'ERROR', 'CANCELLED', 'TIMED_OUT', 'ACTION_REQUIRED', 'STARTUP_FAILURE', 'STALE'}
EXIT = {'complete': 0, 'no_failures': 0, 'partial': 1, 'error': 2, 'superseded': 3, 'cancelled': 130}


class ReadError(Exception):
    pass


def read_command(argv, deadline, limit):
    """Bound both bytes and elapsed time, including a command that stops emitting."""
    end = min(deadline, time.monotonic() + 30)
    if time.monotonic() >= end:
        raise ReadError('collection deadline reached')
    data = bytearray()
    with subprocess.Popen(argv, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL) as process:
        try:
            with selectors.DefaultSelector() as selector:
                selector.register(process.stdout, selectors.EVENT_READ)
                while True:
                    remaining = end - time.monotonic()
                    if remaining <= 0 or not selector.select(remaining):
                        raise ReadError('read command exceeded deadline')
                    chunk = os.read(process.stdout.fileno(), min(65536, limit + 1 - len(data)))
                    if not chunk:
                        break
                    data.extend(chunk)
                    if len(data) > limit:
                        return bytes(data[:limit]), True
            process.wait(timeout=max(0.001, end - time.monotonic()))
            if process.returncode:
                raise ReadError(f'gh read failed with exit {process.returncode}; access, target, or logs may be unavailable')
            return bytes(data), False
        finally:
            if process.poll() is None:
                process.kill()
            process.wait()


def read_json(argv, deadline):
    raw, truncated = read_command(argv, deadline, 4 * 1024 * 1024)
    if truncated:
        raise ReadError('metadata exceeded 4 MiB limit')
    try:
        return json.loads(raw)
    except (ValueError, UnicodeError) as exc:
        raise ReadError('invalid JSON metadata') from exc


def api(path):
    return ['gh', 'api', '--hostname', 'github.com', path]


def snapshot(args, deadline):
    return read_json(['gh', 'pr', 'view', str(args.pr), '--repo', 'github.com/' + args.repo,
                      '--json', 'headRefOid,state,statusCheckRollup,url'], deadline)


def failed_checks(snapshot):
    failed = []
    for check in snapshot.get('statusCheckRollup') or []:
        if not isinstance(check, dict):
            raise ReadError('unknown check metadata')
        if 'status' in check:
            if check['status'] == 'COMPLETED':
                state = check.get('conclusion')
            elif check['status'] in {'QUEUED', 'IN_PROGRESS', 'WAITING', 'REQUESTED', 'PENDING'}:
                state = 'PENDING'
            else:
                raise ReadError('unknown check status')
        else:
            state = check.get('state')
        if state not in FAILURES | {'SUCCESS', 'NEUTRAL', 'SKIPPED', 'PENDING', 'EXPECTED'}:
            raise ReadError('unknown check conclusion')
        if state in FAILURES:
            failed.append({'name': check.get('name', check.get('context')), 'state': state,
                           'url': check.get('detailsUrl', check.get('targetUrl'))})
    return sorted(failed, key=lambda item: (item['name'] or '', item['url'] or '', item['state']))


def job_ids(url, repo):
    if not isinstance(url, str):
        return None
    try:
        parsed = urlparse(url)
    except ValueError:
        return None
    if parsed.scheme != 'https' or parsed.netloc.lower() != 'github.com':
        return None
    pattern = '/' + re.escape(repo) + r'/(?:actions/runs/(\d+)/job/(\d+)|runs/(\d+)/jobs/(\d+))/?'
    match = re.fullmatch(pattern, parsed.path, re.IGNORECASE)
    if not match:
        return None
    parts = match.groups()
    return int(parts[0] or parts[2]), int(parts[1] or parts[3])


def excerpts(raw):
    lines = raw.decode('utf-8', errors='replace').splitlines()
    matches = set()
    for index, line in enumerate(lines):
        if re.search(r'##\[error\]|\b(error|failed|failure|panic|traceback|assertionerror)\b', line, re.IGNORECASE):
            matches.update(range(max(0, index - 1), min(len(lines), index + 3)))
            if len(matches) >= 80:
                break
    return [{'line': index + 1, 'text': lines[index][:400]} for index in sorted(matches)[:80]]


def write_private(path, data):
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(descriptor, 'wb') as output:
        output.write(data)


def collect(args):
    deadline = time.monotonic() + args.timeout
    packet = {'status': 'error', 'target': {'repo': args.repo, 'pr': args.pr, 'sha': args.sha},
              'jobs': [], 'gaps': []}
    runs = {}
    try:
        initial = snapshot(args, deadline)
        packet['initial'] = initial
        if initial['headRefOid'] != args.sha:
            packet['status'] = 'superseded'
            return packet
        failed = failed_checks(initial)
        packet['failed_checks'] = failed
        for check in failed[:args.max_jobs]:
            entry = {'check': check}
            packet['jobs'].append(entry)
            ids = job_ids(check['url'], args.repo)
            if ids is None:
                packet['gaps'].append({'check': check, 'reason': 'unsupported check provider or job URL'})
                continue
            run_id, job_id = ids
            try:
                job = read_json(api(f'repos/{args.repo}/actions/jobs/{job_id}'), deadline)
                run = read_json(api(f'repos/{args.repo}/actions/runs/{run_id}'), deadline)
                if type(job.get('run_attempt')) is not int or type(run.get('run_attempt')) is not int:
                    raise ReadError('job/run attempt metadata unavailable')
                if (job['id'] != job_id or job['run_id'] != run_id or run['id'] != run_id
                        or job['head_sha'] != args.sha or run['head_sha'] != args.sha
                        or job['run_attempt'] != run['run_attempt']):
                    packet['status'] = 'superseded'
                    packet['gaps'].append({'check': check, 'reason': 'job/run revision or attempt mismatch'})
                    return packet
                if run_id in runs and runs[run_id] != run['run_attempt']:
                    packet['status'] = 'superseded'
                    return packet
                runs[run_id] = run['run_attempt']
                entry.update(run_id=run_id, job_id=job_id, attempt=job['run_attempt'],
                             failed_steps=[{'name': step['name'], 'number': step['number'],
                                            'conclusion': step['conclusion']}
                                           for step in job.get('steps', [])
                                           if (step.get('conclusion') or '').upper() in FAILURES])
                if job['status'] != 'completed' or (job.get('conclusion') or '').upper() not in FAILURES:
                    raise ReadError('job no longer has a completed failure')
                raw, truncated = read_command(api(f'repos/{args.repo}/actions/jobs/{job_id}/logs'),
                                              deadline, args.max_log_bytes)
                log_name = f'job-{job_id}-attempt-{job["run_attempt"]}.log'
                log_path = args.output_dir / log_name
                # Multiple checks can link to the same job; reuse only identical captured bytes.
                if log_path.exists():
                    if log_path.read_bytes() != raw:
                        raise ReadError('duplicate job returned different log bytes')
                else:
                    write_private(log_path, raw)
                entry.update(log=str(log_path), bytes=len(raw), truncated=truncated,
                             sha256=hashlib.sha256(raw).hexdigest(), excerpts=excerpts(raw))
                if truncated:
                    packet['gaps'].append({'check': check, 'reason': 'log truncated at byte limit'})
            except (ReadError, OSError, KeyError, TypeError, subprocess.TimeoutExpired) as exc:
                packet['gaps'].append({'check': check, 'reason': str(exc)})
        if len(failed) > args.max_jobs:
            packet['gaps'].append({'reason': 'failed-job limit reached', 'omitted_checks': failed[args.max_jobs:]})
        final = snapshot(args, deadline)
        packet['final'] = final
        if final['headRefOid'] != args.sha or failed_checks(final) != failed:
            packet['status'] = 'superseded'
            return packet
        for run_id, attempt in runs.items():
            latest = read_json(api(f'repos/{args.repo}/actions/runs/{run_id}'), deadline)
            if latest['head_sha'] != args.sha or latest['run_attempt'] != attempt:
                packet['status'] = 'superseded'
                return packet
        packet['status'] = 'partial' if packet['gaps'] else 'complete' if failed else 'no_failures'
    except KeyboardInterrupt:
        packet['status'] = 'cancelled'
    except (ReadError, OSError, KeyError, TypeError, subprocess.TimeoutExpired) as exc:
        packet['gaps'].append({'reason': str(exc), 'phase': 'collection or final freshness check'})
        packet['status'] = 'partial' if 'initial' in packet else 'error'
    return packet


def positive(value):
    parsed = float(value)
    if not math.isfinite(parsed) or parsed <= 0:
        raise argparse.ArgumentTypeError('must be positive and finite')
    return parsed


def positive_int(value):
    parsed = int(value)
    if parsed <= 0:
        raise argparse.ArgumentTypeError('must be positive')
    return parsed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', required=True)
    parser.add_argument('--pr', type=positive_int, required=True)
    parser.add_argument('--sha', required=True)
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--timeout', type=positive, required=True)
    parser.add_argument('--max-jobs', type=positive_int, default=5)
    parser.add_argument('--max-log-bytes', type=positive_int, default=2 * 1024 * 1024)
    args = parser.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', args.repo):
        parser.error('use OWNER/REPO')
    if not re.fullmatch(r'[0-9a-f]{40}', args.sha):
        parser.error('--sha must be a full lowercase commit SHA')
    if not args.output_dir.is_absolute():
        parser.error('--output-dir must be absolute')
    def cancel(*_):
        raise KeyboardInterrupt
    signal.signal(signal.SIGTERM, cancel)
    try:
        args.output_dir.mkdir(mode=0o700, parents=True, exist_ok=False)
        packet = collect(args)
        packet['observed_at'] = datetime.now(timezone.utc).isoformat()
        path = args.output_dir / 'packet.json'
        write_private(path, (json.dumps(packet, indent=2) + '\n').encode())
        print(json.dumps({'status': packet['status'], 'packet': str(path),
                          'failed_checks': len(packet.get('failed_checks', [])), 'gaps': len(packet['gaps'])}))
        return EXIT[packet['status']]
    except OSError as exc:
        print(json.dumps({'status': 'error', 'reason': str(exc)}))
        return EXIT['error']


if __name__ == '__main__':
    raise SystemExit(main())
