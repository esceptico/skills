"""Exercise flexible ledger layouts without weakening structural error checks."""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]


class LedgerValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        intent = root / 'intent.txt'
        intent.write_text('Assess this idea. No implementation is requested.')
        subprocess.run([
            sys.executable, str(SKILL / 'scripts/create_ledger.py'),
            '--root', str(root), '--title', 'Research', '--repo', str(root),
            '--intent-file', str(intent),
        ], check=True, capture_output=True, text=True)
        self.ledger = root / 'research'

    def validate(self):
        return subprocess.run([
            sys.executable, str(SKILL / 'scripts/validate_ledger.py'),
            str(self.ledger), '--repo', self.temp.name,
        ], capture_output=True, text=True)

    def test_generated_ledger_is_valid(self):
        result = self.validate()
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_research_only_completion_can_use_prose(self):
        (self.ledger / 'implementation.md').unlink()
        (self.ledger / 'verification.md').unlink()
        (self.ledger / 'research.md').write_text(
            '# Findings\nThe reviewed design meets the stated constraints.\n')
        readme = self.ledger / 'README.md'
        readme.write_text(readme.read_text().replace('| researching |', '| complete |')
                          + '\nEvidence is recorded in research.md. No execution was requested.\n')
        result = self.validate()
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn('review completion evidence', result.stdout)

    def test_missing_readme_is_invalid(self):
        (self.ledger / 'README.md').unlink()
        self.assertNotEqual(self.validate().returncode, 0)

    def test_invalid_state_is_rejected(self):
        readme = self.ledger / 'README.md'
        readme.write_text(readme.read_text().replace('| researching |', '| invented |'))
        self.assertNotEqual(self.validate().returncode, 0)

    def test_unresolved_template_is_rejected(self):
        (self.ledger / 'research.md').write_text('{{TITLE}}')
        self.assertNotEqual(self.validate().returncode, 0)


if __name__ == '__main__':
    unittest.main()
