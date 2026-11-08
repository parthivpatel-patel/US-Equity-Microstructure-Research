import hashlib
import tempfile
import unittest
from pathlib import Path
from phase250_provenance_bridge import evaluate_historical_input


class BridgeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / 'source.bin'
        self.path.write_bytes(b'synthetic only')
        self.manifest = dict(source_url='https://example.org/synthetic',
            retrieved_utc='2026-11-08T00:00:00Z',
            source_sha256=hashlib.sha256(self.path.read_bytes()).hexdigest(),
            calendar_reference='unverified', treatment_reference='unverified',
            treatment_rule_version='test', license_review='unverified')
        self.attestations = dict(source_authenticated=False,
            calendar_authenticated=False, treatment_authenticated=False,
            license_authorized=False)

    def test_integrity_is_not_authentication(self):
        result = evaluate_historical_input(self.path, self.manifest, self.attestations)
        self.assertTrue(result['integrity']['admitted'])
        self.assertFalse(result['historical_estimation_allowed'])
        self.assertEqual(len(result['failed_checks']), 4)

    def test_tampering_rejects_even_with_all_external_flags(self):
        self.path.write_bytes(b'tampered')
        result = evaluate_historical_input(self.path, self.manifest,
            {k: True for k in self.attestations})
        self.assertFalse(result['historical_estimation_allowed'])
        self.assertEqual(result['failed_checks'], ['byte_integrity'])

    def test_missing_external_flag_rejects(self):
        with self.assertRaises(TypeError):
            evaluate_historical_input(self.path, self.manifest, {'source_authenticated': True})

    def test_string_flag_rejects(self):
        flags = dict(self.attestations, source_authenticated='yes')
        with self.assertRaises(TypeError):
            evaluate_historical_input(self.path, self.manifest, flags)

    def test_conditional_all_true_does_not_prove_authenticity(self):
        result = evaluate_historical_input(self.path, self.manifest,
            {k: True for k in self.attestations})
        self.assertTrue(result['historical_estimation_allowed'])
        self.assertEqual(result['attestation_origin'], 'caller_supplied_not_independently_verified')

    def test_missing_file_rejects(self):
        self.path.unlink()
        result = evaluate_historical_input(self.path, self.manifest,
            {k: True for k in self.attestations})
        self.assertFalse(result['historical_estimation_allowed'])

if __name__ == '__main__':
    unittest.main()
