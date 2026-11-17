import hashlib
from datetime import datetime, timezone
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from phase420_integrated_provenance import integrated_audit

NOW = datetime(2026, 11, 16, tzinfo=timezone.utc)


class IntegratedAuditTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / 'data.csv').write_bytes(b'example fixture\n')
        self.entry = dict(path='data.csv', sha256=hashlib.sha256(b'example fixture\n').hexdigest(),
                          source_url='https://www.sec.gov/example', retrieved_utc='2026-11-15T00:00:00Z',
                          redistribution='unknown', grain='security-date-exchange')

    def run_audit(self):
        return integrated_audit({'sources': [self.entry]}, self.root, NOW)

    def test_valid_fixture_not_authenticated(self):
        r = self.run_audit()
        self.assertEqual(r['status'], 'INTEGRITY_AND_POLICY_PASS_NOT_AUTHENTICATED')
        self.assertFalse(r['source_authenticated'])
        self.assertEqual(r['publication_clearance'], 'NOT_ESTABLISHED')

    def test_hash_mismatch(self):
        self.entry['sha256'] = '0' * 64
        self.assertEqual(self.run_audit()['status'], 'BLOCKED')

    def test_private_host(self):
        self.entry['source_url'] = 'https://127.0.0.1/data'
        r = self.run_audit()
        self.assertEqual(r['integrity_status'], 'PASS')
        self.assertEqual(r['status'], 'BLOCKED')

    def test_future_timestamp(self):
        self.entry['retrieved_utc'] = '2099-01-01T00:00:00Z'
        self.assertEqual(self.run_audit()['status'], 'BLOCKED')

    def test_duplicate_canonical_path(self):
        r = integrated_audit({'sources': [self.entry, dict(self.entry, path='./data.csv')]}, self.root, NOW)
        self.assertEqual(r['status'], 'BLOCKED')

    def test_missing_file(self):
        self.entry['path'] = 'missing.csv'
        self.assertEqual(self.run_audit()['status'], 'BLOCKED')

    def test_unknown_rights_not_clearance(self):
        self.assertEqual(self.run_audit()['publication_clearance'], 'NOT_ESTABLISHED')

    def test_empty_manifest(self):
        r = integrated_audit({'sources': []}, self.root, NOW)
        self.assertEqual(r['status'], 'BLOCKED')


if __name__ == '__main__':
    unittest.main()
