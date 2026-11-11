import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'skills/atlas-quality/scripts/atlas.py'


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def invoke(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True)

    def run_check(self, *args):
        result = self.invoke('run', '--project', str(self.root), '--label', 'test', *args)
        records = list(self.root.glob('.atlas/runs/*/result.json'))
        return result, json.loads(records[-1].read_text(encoding='utf-8')) if records else None

    def test_init_preserves_existing_notes(self):
        self.invoke('init', '--project', str(self.root))
        note = self.root / 'docs/quality/decisions.md'
        note.write_text('existing decision', encoding='utf-8')
        self.assertEqual(self.invoke('init', '--project', str(self.root)).returncode, 0)
        self.assertEqual(note.read_text(), 'existing decision')

    def test_success_is_not_a_pass(self):
        result, record = self.run_check('--', sys.executable, '-c', 'pass')
        self.assertEqual(result.returncode, 0)
        self.assertEqual(record['status'], 'executed')

    def test_failure_preserved(self):
        result, record = self.run_check('--', sys.executable, '-c', 'raise SystemExit(7)')
        self.assertEqual(result.returncode, 1)
        self.assertEqual(record['exit_code'], 7)

    def test_skip_is_not_success(self):
        result, record = self.run_check('--skip', '--reason', 'user deferred')
        self.assertEqual(result.returncode, 2)
        self.assertEqual(record['status'], 'skipped')
        self.assertEqual(record['reason'], 'user deferred')

    def test_missing_tool_is_blocked(self):
        result, record = self.run_check('--', 'atlas-nonexistent-executable-8172')
        self.assertEqual(result.returncode, 2)
        self.assertEqual(record['status'], 'blocked')

    def test_timeout_incomplete(self):
        result, record = self.run_check('--timeout', '0.1', '--', sys.executable, '-c', 'import time; time.sleep(3)')
        self.assertEqual(result.returncode, 2)
        self.assertEqual(record['status'], 'incomplete')

    def test_sensitive_output_and_args_are_not_saved(self):
        result, record = self.run_check('--', sys.executable, '-c', "print('private-marker-928')")
        self.assertNotIn('private-marker-928', json.dumps(record))
        self.assertNotIn('private-marker-928', result.stdout)

    def test_skip_with_command_rejected(self):
        result, record = self.run_check('--skip', '--', sys.executable)
        self.assertEqual(result.returncode, 2)
        self.assertIsNone(record)

    def test_invalid_timeout(self):
        result, record = self.run_check('--timeout', 'nan', '--', sys.executable)
        self.assertEqual(result.returncode, 2)
        self.assertIsNone(record)

    def test_unique_records_do_not_overwrite(self):
        self.run_check('--skip')
        self.run_check('--skip')
        self.assertEqual(len(list(self.root.glob('.atlas/runs/*/result.json'))), 2)

    def test_command_runs_in_project(self):
        result, _ = self.run_check('--', sys.executable, '-c', "from pathlib import Path; Path('target.txt').write_text('ok')")
        self.assertEqual(result.returncode, 0)
        self.assertEqual((self.root / 'target.txt').read_text(), 'ok')

    def test_git_revision_before_evidence(self):
        subprocess.run(['git', 'init', str(self.root)], check=True, capture_output=True)
        subprocess.run(['git', '-C', str(self.root), '-c', 'user.name=Atlas test', '-c', 'user.email=atlas@example.invalid', 'commit', '--allow-empty', '-m', 'fixture'], check=True, capture_output=True)
        _, record = self.run_check('--skip')
        self.assertEqual(len(record['revision']['head']), 40)
        self.assertFalse(record['revision']['dirty'])


if __name__ == '__main__':
    unittest.main()
