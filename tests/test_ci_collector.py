"""CI packet provenance, stale evidence, bounds, and CLI behavior."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'skills/monitor/scripts/ci.py'
spec = importlib.util.spec_from_file_location('ci_collector', SCRIPT)
collector = importlib.util.module_from_spec(spec)
spec.loader.exec_module(collector)
SHA = 'a' * 40

# Local CLI fixture also used for a native-agent forward test. It never contacts GitHub.
FAKE_GH = '''import json, os, pathlib, sys
calls = pathlib.Path(__file__).with_name('calls.jsonl')
with calls.open('a') as f: f.write(json.dumps(sys.argv[1:])+'\\n')
all_calls = [json.loads(line) for line in calls.read_text().splitlines()]
scenario = os.environ.get('COLLECTOR_SCENARIO', 'failure')
args = sys.argv[1:]
sha = 'a'*40
if args[:2] == ['pr','view']:
    reads = sum(a[:2] == ['pr','view'] for a in all_calls)
    head = 'b'*40 if scenario == 'push' and reads > 1 else sha
    url = 'https://github.com/owner/repo/actions/runs/11/job/22'
    if scenario == 'external': url = 'https://ci.example.test/build/22'
    if scenario == 'malformed': url = 'https://[broken'
    check = {'name':'unit','status':'COMPLETED','conclusion':'FAILURE','detailsUrl':url}
    if scenario == 'unknown': check['conclusion'] = 'NEW_STATE'
    checks = [] if scenario == 'none' else [check]
    if scenario == 'limit': checks += [{**check, 'name':'integration', 'detailsUrl':url+'3'}]
    print(json.dumps({'headRefOid':head,'state':'OPEN','url':'https://github.com/owner/repo/pull/42','statusCheckRollup':checks}))
elif args[-1] == 'repos/owner/repo/actions/jobs/22':
    print(json.dumps({'id':22,'run_id':11,'head_sha':'b'*40 if scenario=='wrong-job' else sha,'run_attempt':None if scenario=='missing-attempt' else 1,
      'status':'completed','conclusion':'failure','steps':[{'number':3,'name':'Run unit tests','conclusion':'failure'}]}))
elif args[-1] == 'repos/owner/repo/actions/runs/11':
    reads = sum(a[-1] == args[-1] for a in all_calls)
    print(json.dumps({'id':11,'head_sha':sha,'run_attempt':2 if scenario=='rerun' and reads>1 else 1}))
elif args[-1] == 'repos/owner/repo/actions/jobs/22/logs':
    if scenario == 'unavailable': sys.exit(1)
    print('2026-11-09T00:00:00Z Run pytest')
    print('2026-11-09T00:00:01Z ##[error] FAILED tests/test_release.py::test_config_generation - AssertionError: expected 2, got 1')
    if scenario == 'large': print('x'*100000)
else:
    sys.exit(2)
'''


class Packets(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        gh = self.root / 'gh'
        gh.write_text('#!' + sys.executable + '\n' + FAKE_GH)
        gh.chmod(0o755)
        self.output = self.root / 'evidence'

    def run_scenario(self, scenario='failure', *extra):
        env = {**os.environ, 'PATH': str(self.root) + os.pathsep + os.environ['PATH'],
               'COLLECTOR_SCENARIO': scenario}
        result = subprocess.run([sys.executable, str(SCRIPT), '--repo', 'owner/repo', '--pr', '42',
                                 '--sha', SHA, '--output-dir', str(self.output), '--timeout', '10', *extra],
                                env=env, capture_output=True, text=True, timeout=15)
        packet_path = self.output / 'packet.json'
        packet = json.loads(packet_path.read_text()) if packet_path.exists() else None
        calls = [json.loads(line) for line in (self.root/'calls.jsonl').read_text().splitlines()]
        return result, packet, calls

    def test_complete_packet_has_revision_attempt_sources_and_exact_local_lines(self):
        result, packet, calls = self.run_scenario()
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertEqual(packet['status'], 'complete')
        self.assertEqual(packet['target']['sha'], SHA)
        self.assertEqual(packet['jobs'][0]['attempt'], 1)
        self.assertEqual(packet['jobs'][0]['failed_steps'][0]['name'], 'Run unit tests')
        log = Path(packet['jobs'][0]['log']).read_text().splitlines()
        for excerpt in packet['jobs'][0]['excerpts']:
            self.assertEqual(log[excerpt['line']-1][:400], excerpt['text'])
        self.assertIn('test_config_generation', log[1])
        self.assertEqual(len(result.stdout.splitlines()), 1)
        self.assertEqual(len(calls), 6)
        self.assertEqual(self.output.stat().st_mode & 0o777, 0o700)
        self.assertEqual((self.output/'packet.json').stat().st_mode & 0o777, 0o600)

    def test_head_change_invalidates_current_evidence(self):
        result, packet, _ = self.run_scenario('push')
        self.assertEqual(result.returncode, 3)
        self.assertEqual(packet['status'], 'superseded')
        self.assertEqual(packet['final']['headRefOid'], 'b'*40)

    def test_rerun_same_sha_invalidates_attempt(self):
        result, packet, _ = self.run_scenario('rerun')
        self.assertEqual(result.returncode, 3)
        self.assertEqual(packet['status'], 'superseded')

    def test_wrong_job_revision_prevents_log_download(self):
        result, packet, calls = self.run_scenario('wrong-job')
        self.assertEqual(result.returncode, 3)
        self.assertFalse(any(args[-1].endswith('/logs') for args in calls))
        self.assertNotIn('log', packet['jobs'][0])

    def test_external_provider_is_explicit_gap(self):
        result, packet, calls = self.run_scenario('external')
        self.assertEqual(result.returncode, 1)
        self.assertEqual(packet['status'], 'partial')
        self.assertEqual(len(calls), 2)
        self.assertIn('unsupported', packet['gaps'][0]['reason'])

    def test_malformed_check_url_is_reported_as_gap(self):
        result, packet, calls = self.run_scenario('malformed')
        self.assertEqual(result.returncode, 1)
        self.assertEqual(packet['status'], 'partial')
        self.assertIn('unsupported', packet['gaps'][0]['reason'])
        self.assertEqual(len(calls), 2)

    def test_missing_attempt_is_partial_not_a_claimed_rerun(self):
        result, packet, calls = self.run_scenario('missing-attempt')
        self.assertEqual(result.returncode, 1)
        self.assertEqual(packet['status'], 'partial')
        self.assertIn('metadata unavailable', packet['gaps'][0]['reason'])
        self.assertFalse(any(args[-1].endswith('/logs') for args in calls))

    def test_expired_or_inaccessible_logs_are_partial(self):
        result, packet, _ = self.run_scenario('unavailable')
        self.assertEqual(result.returncode, 1)
        self.assertEqual(packet['status'], 'partial')
        self.assertNotIn('log', packet['jobs'][0])

    def test_log_bytes_are_bounded_and_truncation_is_visible(self):
        result, packet, _ = self.run_scenario('large', '--max-log-bytes', '64')
        self.assertEqual(result.returncode, 1)
        entry = packet['jobs'][0]
        self.assertTrue(entry['truncated'])
        self.assertEqual(Path(entry['log']).stat().st_size, 64)

    def test_job_limit_names_omitted_checks(self):
        result, packet, _ = self.run_scenario('limit', '--max-jobs', '1')
        self.assertEqual(result.returncode, 1)
        gaps = [g for g in packet['gaps'] if 'omitted_checks' in g]
        self.assertEqual(len(gaps[0]['omitted_checks']), 1)

    def test_absent_checks_do_not_claim_ci_success(self):
        result, packet, _ = self.run_scenario('none')
        self.assertEqual(result.returncode, 0)
        self.assertEqual(packet['status'], 'no_failures')
        self.assertEqual(packet['jobs'], [])

    def test_unknown_check_state_is_not_no_failures(self):
        result, packet, _ = self.run_scenario('unknown')
        self.assertEqual(result.returncode, 1)
        self.assertEqual(packet['status'], 'partial')
        self.assertTrue(packet['gaps'])


class ReadBounds(unittest.TestCase):
    def test_silent_command_obeys_deadline(self):
        started = time.monotonic()
        with self.assertRaises(collector.ReadError):
            collector.read_command([sys.executable, '-c', 'import time; time.sleep(30)'], started + 0.1, 100)
        self.assertLess(time.monotonic()-started, 2)

    def test_byte_limit_does_not_require_process_exit(self):
        raw, truncated = collector.read_command([sys.executable, '-c',
            'import sys,time; sys.stdout.write("x"*10000); sys.stdout.flush(); time.sleep(30)'],
            time.monotonic()+2, 32)
        self.assertEqual(len(raw), 32)
        self.assertTrue(truncated)

    def test_url_must_belong_to_target_repo_and_github(self):
        for url in ['https://evil.test/owner/repo/actions/runs/11/job/22',
                    'https://github.com/other/repo/actions/runs/11/job/22',
                    'https://github.com/owner/repo/actions/runs/11']:
            self.assertIsNone(collector.job_ids(url, 'owner/repo'))
        self.assertEqual(collector.job_ids('https://github.com/owner/repo/actions/runs/11/job/22?pr=42', 'owner/repo'), (11,22))


if __name__ == '__main__':
    unittest.main()
