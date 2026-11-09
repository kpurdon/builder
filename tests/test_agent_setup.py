"""Installation lifecycle: do not overwrite user-owned or edited agent definitions."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'skills/setup/scripts/agents.py'
spec = importlib.util.spec_from_file_location('agent_setup', SCRIPT)
setup = importlib.util.module_from_spec(spec)
spec.loader.exec_module(setup)


class AgentSetup(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.destination = self.root / 'profile' / 'agents'
        self.source = self.root / 'builder_monitor.toml'
        self.source.write_text('name = "builder_monitor"\nmodel = "model-one"\n')
        self.target = self.destination / self.source.name

    def run_action(self, action):
        return setup.manage(action, self.destination, self.source)['status']

    def test_check_is_read_only(self):
        self.assertEqual(self.run_action('check'), 'missing')
        self.assertFalse(self.destination.exists())

    def test_install_and_idempotent_update(self):
        self.assertEqual(self.run_action('install'), 'installed')
        before = self.target.stat().st_mtime_ns
        self.assertEqual(self.run_action('check'), 'current')
        self.assertEqual(self.run_action('install'), 'current')
        self.assertEqual(self.target.stat().st_mtime_ns, before)
        self.source.write_text('name = "builder_monitor"\nmodel = "model-two"\n')
        self.assertEqual(self.run_action('check'), 'stale')
        self.assertEqual(self.run_action('install'), 'updated')
        self.assertIn('model-two', self.target.read_text())
        self.assertEqual(self.run_action('check'), 'current')

    def test_local_model_override_survives_update_and_removal(self):
        self.run_action('install')
        changed = self.target.read_text().replace('model-one', 'my-local-model')
        self.target.write_text(changed)
        self.source.write_text('name = "builder_monitor"\nmodel = "model-two"\n')
        for action in ['check', 'install', 'remove']:
            self.assertEqual(self.run_action(action), 'modified')
            self.assertEqual(self.target.read_text(), changed)

    def test_unmarked_file_is_never_adopted_or_overwritten(self):
        self.destination.mkdir(parents=True)
        self.target.write_bytes(self.source.read_bytes())
        for action in ['check', 'install', 'remove']:
            self.assertEqual(self.run_action(action), 'unmanaged')
            self.assertEqual(self.target.read_bytes(), self.source.read_bytes())

    def test_symlink_is_preserved_including_dangling_link(self):
        self.destination.mkdir(parents=True)
        self.target.symlink_to(self.source)
        for action in ['check', 'install', 'remove']:
            self.assertEqual(self.run_action(action), 'conflict')
            self.assertTrue(self.target.is_symlink())
        self.source.unlink()
        # Keep a source file available at a separate path; the destination link is dangling.
        alternate = self.root / 'package' / 'builder_monitor.toml'
        alternate.parent.mkdir()
        alternate.write_text('name = "builder_monitor"\n')
        self.assertEqual(setup.manage('install', self.destination, alternate)['status'], 'conflict')
        self.assertTrue(self.target.is_symlink())

    def test_removal_only_removes_managed_target(self):
        self.run_action('install')
        unrelated = self.destination / 'reviewer.toml'
        unrelated.write_text('name = "reviewer"')
        self.assertEqual(self.run_action('remove'), 'removed')
        self.assertFalse(self.target.exists())
        self.assertTrue(unrelated.exists())
        self.assertEqual(self.run_action('remove'), 'removed')

    def test_real_cli_installs_bundled_definition_and_reports_drift(self):
        def invoke(action):
            p = subprocess.run([sys.executable, str(SCRIPT), action, '--agents-dir', str(self.destination)],
                               capture_output=True, text=True, check=False)
            return p.returncode, json.loads(p.stdout)
        code, outcome = invoke('check')
        self.assertEqual((code, outcome['status']), (1, 'missing'))
        code, outcome = invoke('install')
        self.assertEqual((code, outcome['status']), (0, 'installed'))
        self.assertTrue(self.target.read_bytes().endswith(setup.SOURCE.read_bytes()))
        self.assertEqual(invoke('check')[0], 0)
        self.target.write_text(self.target.read_text() + '\n# user edit\n')
        code, outcome = invoke('install')
        self.assertEqual((code, outcome['status']), (1, 'modified'))


if __name__ == '__main__':
    unittest.main()
