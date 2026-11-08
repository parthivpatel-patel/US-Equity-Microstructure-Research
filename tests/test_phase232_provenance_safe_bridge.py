"""Deterministic provenance regression tests; no empirical data are used."""
import sys
import types
import unittest
from unittest.mock import patch

stub = types.ModuleType('phase230_authenticated_session_bridge')
stub.calendar_gated_matched_hac = lambda *args, **kwargs: {
    'calendar_authenticated': True,
    'calendar_authentication_method': 'caller_attestation_not_independently_verified',
    'calendar_sha256': '0' * 64,
    'estimate': 0.25,
}
with patch.dict(sys.modules, {'phase230_authenticated_session_bridge': stub}):
    from phase232_provenance_safe_bridge import provenance_safe_matched_hac

class ProvenanceTests(unittest.TestCase):
    def test_attestation_not_independent_verification(self):
        r = provenance_safe_matched_hac(source_authenticated=True)
        self.assertTrue(r['calendar_caller_attested'])
        self.assertFalse(r['calendar_independently_verified'])
    def test_legacy_flag_removed(self):
        self.assertNotIn('calendar_authenticated', provenance_safe_matched_hac(source_authenticated=True))
    def test_estimate_preserved(self):
        self.assertEqual(provenance_safe_matched_hac(source_authenticated=True)['estimate'], 0.25)
    def test_provenance_pending(self):
        r = provenance_safe_matched_hac(source_authenticated=True)
        self.assertTrue(r['calendar_source_authentication_pending'])
        self.assertEqual(r['calendar_verification_basis'], 'caller_attestation_and_digest_only')
    def test_unattested_not_promoted(self):
        r = provenance_safe_matched_hac(source_authenticated=False)
        self.assertFalse(r['calendar_caller_attested'])
        self.assertFalse(r['calendar_independently_verified'])

if __name__ == '__main__':
    unittest.main()
