"""Exercise the ledger CLI against throwaway git repositories."""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / 'ledger.py'


def run(*args, cwd, stdin=None):
    return subprocess.run([sys.executable, str(SCRIPT), *args], cwd=cwd, input=stdin,
                          capture_output=True, text=True)


class LedgerTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.repo = Path(temp.name)
        self.git('init', '-q')
        self.git('commit', '-q', '--allow-empty', '-m', 'init')
        result = run('new', 'Do X', '--intent-file', '-', cwd=self.repo, stdin='Assess this idea.\n')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.ledger = self.repo / 'docs/ledgers/do-x'

    def git(self, *args):
        subprocess.run(['git', '-c', 'user.name=t', '-c', 'user.email=t@t', *args],
                       cwd=self.repo, check=True, capture_output=True)

    def check(self):
        return run('check', str(self.ledger), cwd=self.repo)

    def edit(self, name, old, new):
        path = self.ledger / name
        path.write_text(path.read_text().replace(old, new))

    def test_new_ledger_is_valid_and_captures_intent(self):
        result = self.check()
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn('Assess this idea.', (self.ledger / 'README.md').read_text())

    def test_new_refuses_to_overwrite(self):
        self.assertNotEqual(run('new', 'Do X', cwd=self.repo).returncode, 0)

    def test_missing_intent_is_an_error(self):
        run('new', 'Other', cwd=self.repo)
        result = run('check', 'docs/ledgers/other', cwd=self.repo)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('not captured', result.stdout)

    def test_committing_the_ledger_alone_is_not_drift(self):
        self.git('add', '-A')
        self.git('commit', '-qm', 'ledger')
        self.assertNotIn('changed since', self.check().stdout)

    def test_other_ledgers_are_not_drift(self):
        run('new', 'Other', cwd=self.repo)
        self.git('add', '-A')
        self.git('commit', '-qm', 'two ledgers')
        self.assertNotIn('changed since', self.check().stdout)

    def test_code_change_is_drift_until_sync(self):
        (self.repo / 'app.py').write_text('x = 1\n')
        self.git('add', '-A')
        self.git('commit', '-qm', 'code')
        self.assertIn('1 file changed since', self.check().stdout)
        self.assertEqual(run('sync', str(self.ledger), cwd=self.repo).returncode, 0)
        self.assertNotIn('changed since', self.check().stdout)

    def test_list_finds_gitignored_ledgers(self):
        (self.repo / '.gitignore').write_text('docs/\n')
        self.assertIn('docs/ledgers/do-x', run('list', cwd=self.repo).stdout)

    def test_checked_item_needs_passing_evidence(self):
        self.edit('implementation.md', '- [ ] **I-01', '- [x] **I-01')
        self.assertIn('checked without passing evidence: I-01', self.check().stdout)
        self.edit('verification.md', '| --- | --- | --- | --- | --- | --- |',
                  '| --- | --- | --- | --- | --- | --- |\n| V-01 | I-01 | `make test` | 0 failures | 0 failures | pass |')
        self.assertNotIn('without passing evidence', self.check().stdout)

    def test_complete_with_failing_evidence_warns(self):
        self.edit('verification.md', '| --- | --- | --- | --- | --- | --- |',
                  '| --- | --- | --- | --- | --- | --- |\n| V-01 | I-01 | test | ok | broke | fail |')
        self.edit('README.md', '| researching |', '| complete |')
        self.assertIn('failing or open evidence', self.check().stdout)

    def test_research_only_completion_is_valid(self):
        (self.ledger / 'implementation.md').unlink()
        (self.ledger / 'verification.md').unlink()
        self.edit('README.md', '| researching |', '| complete |')
        result = self.check()
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn('0 warning(s)', result.stdout)

    def test_invalid_and_legacy_states(self):
        self.edit('README.md', '| researching |', '| invented |')
        self.assertNotEqual(self.check().returncode, 0)
        self.edit('README.md', '| invented |', '| needs-input |')
        result = self.check()
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("use 'blocked'", result.stdout)

    def test_missing_readme_is_invalid(self):
        (self.ledger / 'README.md').unlink()
        self.assertNotEqual(self.check().returncode, 0)

    def test_render_escapes_content(self):
        self.edit('README.md', 'Begin the first scoped research pass.', '<script>alert(1)</script>')
        out = self.repo / 'view.html'
        self.assertEqual(run('render', '-o', str(out), cwd=self.repo).returncode, 0)
        page = out.read_text()
        self.assertIn('&lt;script&gt;', page)
        self.assertNotIn('<script>alert', page)
        self.assertNotIn('{{', page)


if __name__ == '__main__':
    unittest.main()
