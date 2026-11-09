"""Regression cases for stale evidence, bounded waits, and CLI integration."""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / 'skills/monitor/scripts/wait.py'
spec = importlib.util.spec_from_file_location('monitor_wait', SCRIPT)
monitor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(monitor)
SHA = 'a' * 40


def check(name='unit', status='COMPLETED', conclusion='SUCCESS'):
    return dict(name=name, status=status, conclusion=conclusion, detailsUrl='https://example.test/check')


def deployment(image='api@sha256:new', generation=2, observed=2, **replicas):
    return {'metadata': {'uid': 'deployment-1', 'generation': generation},
            'spec': {'replicas': 2, 'template': {'metadata': {'annotations': {'config-revision': 'new'}}, 'spec': {'containers': [{'name': 'api', 'image': image}]}}},
            'status': {'observedGeneration': observed, 'replicas': 2, 'updatedReplicas': 2,
                       'readyReplicas': 2, 'availableReplicas': 2, **replicas}}


class CI(unittest.TestCase):
    def test_absent_required_check_never_passes(self):
        self.assertEqual(monitor.ci_state([], ['unit'])['status'], 'pending')
        self.assertEqual(monitor.ci_state([check()], ['unit', 'integration'])['status'], 'pending')

    def test_running_failure_and_legacy_status(self):
        self.assertEqual(monitor.ci_state([check(status='IN_PROGRESS')], ['unit'])['status'], 'pending')
        self.assertEqual(monitor.ci_state([check(conclusion='FAILURE')], ['unit'])['status'], 'failed')
        self.assertEqual(monitor.ci_state([{'context': 'unit', 'state': 'SUCCESS'}], ['unit'])['status'], 'ready')

    def test_ambiguous_or_unknown_evidence_escalates(self):
        for checks in [[check(), check()], [check(conclusion='NEW_ENUM')]]:
            with self.assertRaises(ValueError):
                monitor.ci_state(checks, ['unit'])

    def test_head_change_during_success_read_supersedes_result(self):
        args = argparse.Namespace(action='ci', repo='owner/repo', pr=42, sha=SHA, check=['unit'])
        first = dict(headRefOid=SHA, state='OPEN', statusCheckRollup=[check()])
        second = dict(headRefOid='b' * 40, state='OPEN')
        with patch.object(monitor, 'pr_target', side_effect=[first, second]):
            self.assertEqual(monitor.github(args, 100)['status'], 'superseded')

    def test_closed_pr_stops(self):
        self.assertEqual(monitor.changed_pr(dict(headRefOid=SHA, state='CLOSED'), SHA)['status'], 'superseded')


class Reviews(unittest.TestCase):
    def setUp(self):
        self.review = dict(id=12, state='CHANGES_REQUESTED', commit_id=SHA,
                           user={'login': 'reviewer'}, submitted_at='2026-11-09T15:00:00Z',
                           html_url='https://example.test/review/12')

    def test_filters_commit_author_and_submission(self):
        for changes in [dict(commit_id='old'), dict(user={'login': 'other'}),
                        dict(state='PENDING'), dict(state='DISMISSED')]:
            self.assertEqual(monitor.review_state([{**self.review, **changes}], SHA, 'reviewer')['status'], 'pending')
        self.assertEqual(monitor.review_state([self.review], SHA, 'reviewer', monitor.timestamp('2026-11-09T16:00:00Z'))['status'], 'pending')

    def test_changes_requested_is_arrival_not_approval(self):
        actual = monitor.review_state([self.review], SHA, 'reviewer')
        self.assertEqual(actual['status'], 'ready')
        self.assertEqual(actual['review']['state'], 'CHANGES_REQUESTED')


class Rollouts(unittest.TestCase):
    def setUp(self):
        self.watcher = monitor.Rollout({'api': 'api@sha256:new'}, 'annotations', 'config-revision', 'new')

    def test_old_healthy_revision_then_target_converges(self):
        self.assertEqual(self.watcher.observe(deployment(image='api@sha256:old'))['status'], 'pending')
        self.assertEqual(self.watcher.observe(deployment(observed=1))['status'], 'pending')
        self.assertEqual(self.watcher.observe(deployment(readyReplicas=1))['status'], 'pending')
        self.assertEqual(self.watcher.observe(deployment())['status'], 'ready')

    def test_same_image_old_config_does_not_pass(self):
        old = deployment()
        old['spec']['template']['metadata']['annotations']['config-revision'] = 'old'
        self.assertEqual(self.watcher.observe(old)['status'], 'pending')
        self.assertEqual(self.watcher.observe(deployment(generation=3, observed=2))['status'], 'pending')
        self.assertEqual(self.watcher.observe(deployment(generation=3, observed=3))['status'], 'ready')

    def test_unexpected_config_supersedes_even_with_same_image(self):
        old = deployment()
        old['spec']['template']['metadata']['annotations']['config-revision'] = 'old'
        self.watcher.observe(old)
        old['spec']['template']['metadata']['annotations']['config-revision'] = 'other'
        self.assertEqual(self.watcher.observe(old)['status'], 'superseded')

    def test_extra_old_replica_blocks_success(self):
        self.assertEqual(self.watcher.observe(deployment(replicas=3))['status'], 'pending')

    def test_unexpected_template_or_recreation_supersedes(self):
        self.watcher.observe(deployment(image='api@sha256:old'))
        self.assertEqual(self.watcher.observe(deployment(image='api@sha256:other'))['status'], 'superseded')
        recreated = deployment()
        recreated['metadata']['uid'] = 'deployment-2'
        self.assertEqual(self.watcher.observe(recreated)['status'], 'superseded')

    def test_target_replaced_before_readiness(self):
        self.watcher.observe(deployment(readyReplicas=1))
        self.assertEqual(self.watcher.observe(deployment(image='api@sha256:old'))['status'], 'superseded')

    def test_deadline_failure_and_zero_replicas(self):
        stalled = deployment()
        stalled['status']['conditions'] = [dict(type='Progressing', status='False', reason='ProgressDeadlineExceeded')]
        self.assertEqual(self.watcher.observe(stalled)['status'], 'failed')
        scaled_down = deployment(replicas=0, updatedReplicas=0, readyReplicas=0, availableReplicas=0)
        scaled_down['spec']['replicas'] = 0
        self.assertEqual(self.watcher.observe(scaled_down)['status'], 'pending')

    def test_partial_container_map_does_not_pass(self):
        extra = deployment()
        extra['spec']['template']['spec']['containers'].append(dict(name='sidecar', image='sidecar:v1'))
        self.assertEqual(self.watcher.observe(extra)['status'], 'pending')


class WaitLoop(unittest.TestCase):
    def test_repeated_pending_times_out_with_last_evidence(self):
        now = [0]
        def sleep(seconds):
            now[0] += seconds
        outcome = monitor.wait(lambda _: monitor.result('pending', head=SHA), 5, 3,
                               clock=lambda: now[0], sleep=sleep)
        self.assertEqual(now[0], 5)
        self.assertEqual(outcome['status'], 'timeout')
        self.assertEqual(outcome['last']['head'], SHA)

    def test_error_and_cancellation_stop_without_retry(self):
        for exception, expected in [(ValueError('bad evidence'), 'error'), (KeyboardInterrupt(), 'cancelled')]:
            def probe(_):
                raise exception
            self.assertEqual(monitor.wait(probe, 5, 1)['status'], expected)


class CLI(unittest.TestCase):
    def test_pending_then_ready_runs_without_model_polling(self):
        # A fake gh records every read and makes the second snapshot green.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            gh = root / 'gh'
            gh.write_text('#!' + sys.executable + '\n' + '''
import json, os, pathlib, sys
p=pathlib.Path(os.environ['MONITOR_CALLS'])
with p.open('a') as f: f.write(json.dumps(sys.argv[1:])+'\\n')
count=len(p.read_text().splitlines())
d={'headRefOid':'a'*40,'state':'OPEN'}
if 'headRefOid,state,statusCheckRollup' in sys.argv:
 d['statusCheckRollup']=[{'name':'unit','status':'IN_PROGRESS' if count==1 else 'COMPLETED','conclusion':'SUCCESS'}]
print(json.dumps(d))
''')
            gh.chmod(0o755)
            calls = root / 'calls'
            env = {**os.environ, 'PATH': str(root) + os.pathsep + os.environ['PATH'], 'MONITOR_CALLS': str(calls)}
            proc = subprocess.run([sys.executable, str(SCRIPT), 'ci', '--repo', 'owner/repo',
                                   '--pr', '42', '--sha', SHA, '--check', 'unit',
                                   '--timeout', '5', '--interval', '0.01'], env=env,
                                  capture_output=True, text=True, timeout=10)
            self.assertEqual(proc.returncode, 0, proc.stderr + proc.stdout)
            self.assertEqual(len(proc.stdout.splitlines()), 1)
            self.assertEqual(json.loads(proc.stdout)['status'], 'ready')
            self.assertEqual(len(calls.read_text().splitlines()), 3)

    def test_invalid_target_and_deadline_do_not_launch_reads(self):
        for value in ['0', 'nan', 'inf']:
            proc = subprocess.run([sys.executable, str(SCRIPT), 'ci', '--repo', 'owner/repo',
                                   '--pr', '42', '--sha', SHA, '--check', 'unit', '--timeout', value],
                                  capture_output=True, text=True)
            self.assertEqual(proc.returncode, 2)


if __name__ == '__main__':
    unittest.main()
