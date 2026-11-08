import importlib.util
import pathlib
import sys
import types
import unittest
from unittest.mock import Mock

ROOT = pathlib.Path(__file__).resolve().parents[1] / 'scripts'
sys.path.insert(0, str(ROOT))
bridge = types.ModuleType('phase232_provenance_safe_bridge')
bridge.provenance_safe_matched_hac = Mock(return_value={'estimate': 0.0, 'calendar_authenticated': True})
sys.modules['phase232_provenance_safe_bridge'] = bridge
spec = importlib.util.spec_from_file_location('phase235', ROOT/'phase235_structural_preflight.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class PreflightTests(unittest.TestCase):
    def setUp(self):
        bridge.provenance_safe_matched_hac.reset_mock()
        self.k = dict(calendar=['2025-09-02','2025-09-03','2025-09-04'],
                      source_url='https://example.org/calendar.csv',
                      retrieved_at='2026-11-08T07:00:00Z', raw_sha256='a'*64,
                      source_authenticated=True)
    def run_gate(self, sessions=None, early=None, late=None, **updates):
        kw = dict(self.k); kw.update(updates)
        return mod.structurally_gated_matched_hac([], [], sessions or ['2025-09-02','2025-09-03'],
                        [], early if early is not None else ['2025-09-02'],
                        late if late is not None else ['2025-09-03'], 1, **kw)
    def test_valid_fixture_metadata_never_claims_independent_verification(self):
        r=self.run_gate()
        self.assertFalse(r['calendar_independently_verified'])
        self.assertNotIn('calendar_authenticated',r)
        self.assertTrue(r['calendar_structurally_validated'])
        bridge.provenance_safe_matched_hac.assert_called_once()
    def test_labor_day_rejected_as_absent(self):
        with self.assertRaises(ValueError):
            self.run_gate(sessions=['2025-09-01','2025-09-02'],early=['2025-09-01'],late=['2025-09-02'])
        bridge.provenance_safe_matched_hac.assert_not_called()
    def test_weekend_roster_rejected(self):
        with self.assertRaises(ValueError): self.run_gate(calendar=['2025-09-06'])
        bridge.provenance_safe_matched_hac.assert_not_called()
    def test_unordered_roster_rejected(self):
        with self.assertRaises(ValueError): self.run_gate(calendar=['2025-09-03','2025-09-02'])
    def test_naive_timestamp_rejected(self):
        with self.assertRaises(ValueError): self.run_gate(retrieved_at='2026-11-08T07:00:00')
    def test_attestation_required(self):
        with self.assertRaises(ValueError): self.run_gate(source_authenticated=False)
        bridge.provenance_safe_matched_hac.assert_not_called()
    def test_unpartitioned_sessions_rejected(self):
        with self.assertRaises(ValueError): self.run_gate(late=[])
    def test_duplicate_sessions_rejected(self):
        with self.assertRaises(ValueError): self.run_gate(sessions=['2025-09-02','2025-09-02'],late=['2025-09-02'])
    def test_source_digest_format_rejected(self):
        with self.assertRaises(ValueError): self.run_gate(raw_sha256='invalid')

if __name__ == '__main__': unittest.main()
