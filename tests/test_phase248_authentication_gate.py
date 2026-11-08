import hashlib
import tempfile
import unittest
from pathlib import Path
from phase248_authentication_gate import audit_input, REQUIRED

class GateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / 'fixture.csv'
        self.path.write_bytes(b'date,value\n2025-10-01,1\n')
        self.manifest = {k: 'fixture-only' for k in REQUIRED}
        self.manifest['source_sha256'] = hashlib.sha256(self.path.read_bytes()).hexdigest()

    def test_complete_digest_is_not_authentication(self):
        result = audit_input(self.path, self.manifest)
        self.assertTrue(result['admitted'])
        self.assertFalse(result['independent_source_authentication'])
        self.assertFalse(result['redistribution_authorized'])

    def test_missing_field_rejected(self):
        del self.manifest['calendar_reference']
        self.assertFalse(audit_input(self.path, self.manifest)['admitted'])

    def test_tampering_rejected(self):
        self.path.write_bytes(b'tampered')
        self.assertEqual(audit_input(self.path, self.manifest)['reason'], 'digest mismatch')

    def test_bad_digest_rejected(self):
        self.manifest['source_sha256'] = 'abc'
        self.assertEqual(audit_input(self.path, self.manifest)['reason'], 'invalid sha256')

    def test_missing_file_rejected(self):
        self.path.unlink()
        self.assertEqual(audit_input(self.path, self.manifest)['reason'], 'source file unavailable')

if __name__ == '__main__':
    unittest.main()
