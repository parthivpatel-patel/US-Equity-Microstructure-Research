"""Orchestration contract tests using isolated stubs, NOT SEC observations."""
import hashlib
import sys
import types
import unittest

gate = types.ModuleType('phase229_session_gate')
def validate_sessions(requested, calendar, *, source, expected_sha256):
    if requested != sorted(set(requested)) or not set(requested).issubset(calendar):
        raise ValueError('invalid sessions')
    digest = hashlib.sha256(('\n'.join(calendar)+'\n').encode()).hexdigest()
    if digest != expected_sha256:
        raise ValueError('bad digest')
    return {'calendar_sha256':digest,'calendar_source':source}
gate.validate_sessions = validate_sessions
bridge = types.ModuleType('phase226_matched_hac_bridge')
bridge.matched_full_series_hac = lambda *args: {'estimate':0.25}
sys.modules['phase229_session_gate'] = gate
sys.modules['phase226_matched_hac_bridge'] = bridge
from phase230_authenticated_session_bridge import calendar_gated_matched_hac

class ContractTests(unittest.TestCase):
    def setUp(self):
        self.cal=['2025-09-02','2025-09-03']
        self.kw=dict(calendar=self.cal, calendar_source='fixture-only',calendar_sha256=hashlib.sha256(('\n'.join(self.cal)+'\n').encode()).hexdigest(),source_authenticated=True)
    def call(self,**overrides):
        kw=dict(self.kw); kw.update(overrides)
        return calendar_gated_matched_hac([],[],self.cal,[],self.cal[:1],self.cal[1:],0,**kw)
    def test_attestation_required(self):
        with self.assertRaises(ValueError): self.call(source_authenticated=False)
    def test_digest_required(self):
        with self.assertRaises(ValueError): self.call(calendar_sha256='0'*64)
    def test_valid_fixture(self):
        r=self.call(); self.assertEqual(r['estimate'],0.25); self.assertTrue(r['calendar_authenticated'])
    def test_metadata_not_independent_verification(self):
        self.assertEqual(self.call()['calendar_authentication_method'],'caller_attestation_not_independently_verified')
    def test_missing_session(self):
        with self.assertRaises(ValueError): self.call(calendar=['2025-09-02'])

if __name__=='__main__': unittest.main()
