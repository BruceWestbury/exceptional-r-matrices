"""Ensure the comparison cannot silently accept stale data or a missing worker."""
import contextlib
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from check_macaulay2_data import Runner


class CheckerFailures(unittest.TestCase):
    def test_zero_exit_without_completion_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fake = root / 'fake-M2'
            fake.write_text('#!/bin/sh\nexit 0\n')
            fake.chmod(0o755)
            runner = Runner(str(fake), root)
            with contextlib.redirect_stdout(io.StringIO()), self.assertRaises(RuntimeError):
                runner.run('missing_output', 'exit 0;')
            self.assertEqual(runner.stages[0]['status'], 'FAIL')

    @unittest.skipUnless(shutil.which('M2'), 'requires Macaulay2')
    def test_changed_y2_sign_is_reported_with_coordinates(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            data = root / 'data'
            shutil.copytree(ROOT / 'data', data)
            path = data / 'representations/Y2.json'
            doc = json.loads(path.read_text())
            s1 = next(m for m in doc['matrices'] if m['operator'] == 'S1')
            entry = next(e for e in s1['entries'] if e[:2] == [1, 0])
            entry[2] = '-(' + entry[2] + ')'
            path.write_text(json.dumps(doc))
            report = root / 'result.json'
            result = subprocess.run(
                [sys.executable, '-B', str(ROOT / 'tools/check_macaulay2_data.py'),
                 '--data-root', str(data), '--representation', 'Y2', '--output', str(report)],
                cwd=root, capture_output=True, text=True, timeout=90)
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            saved = json.loads(report.read_text())
            self.assertEqual(saved['status'], 'FAIL')
            self.assertEqual(saved['stages'][0]['stage'], 'Y2_paper')
            self.assertIn('EDFAIL|ordinary/S1|1|0|', result.stderr)


if __name__ == '__main__':
    unittest.main()
