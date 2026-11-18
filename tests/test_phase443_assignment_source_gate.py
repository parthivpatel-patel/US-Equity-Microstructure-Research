"""Contract tests; synthetic data only, no historical SEC inference."""
import hashlib
import importlib.util
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import patch

HERE = Path(__file__).resolve().parents[1] / 'scripts'
fake439 = types.ModuleType('phase439_verified_entrypoint')
fake442 = types.ModuleType('phase442_assignment_gate')
fake439.evaluate_verified_bytes = lambda raw: {'source_sha256': hashlib.sha256(raw).hexdigest(), 'source_bytes': len(raw), 'pass': True}
fake442.evaluate = lambda rows: {'pass': True, 'observations': len(list(rows))}
sys.modules['phase439_verified_entrypoint'] = fake439
sys.modules['phase442_assignment_gate'] = fake442
spec = importlib.util.spec_from_file_location('phase443', HERE / 'phase443_assignment_source_gate.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
RAW = b'date,security,exchange,match_group,treated\n2025-10-01,ABC,X,1,1\n'

class ContractTests(unittest.TestCase):
    def test_valid_binds_exact_bytes(self):
        r = mod.evaluate_bytes(RAW)
        self.assertTrue(r['pass'])
        self.assertEqual(r['assignment_scope']['source_sha256'], hashlib.sha256(RAW).hexdigest())
        self.assertEqual(r['assignment_scope']['source_bytes'], len(RAW))
        self.assertFalse(r['treatment_authenticated'])
    def test_assignment_failure_fails_closed(self):
        with patch.object(mod, 'assignment_audit', return_value={'pass': False}):
            self.assertFalse(mod.evaluate_bytes(RAW)['pass'])
    def test_upstream_failure_fails_closed(self):
        with patch.object(mod, 'evaluate_verified_bytes', return_value={'pass': False, 'source_sha256': 'x', 'source_bytes': 1}):
            self.assertFalse(mod.evaluate_bytes(RAW)['pass'])
    def test_structural_failure_prevents_assignment(self):
        with patch.object(mod, 'evaluate_verified_bytes', side_effect=ValueError('invalid CSV')):
            with patch.object(mod, 'assignment_audit') as check:
                with self.assertRaises(ValueError): mod.evaluate_bytes(RAW)
                check.assert_not_called()
    def test_bom_accepted_by_parser(self):
        self.assertEqual(mod.evaluate_bytes(b'\xef\xbb\xbf'+RAW)['assignment_scope']['observations'], 1)
    def test_missing_required_fields_fails_in_real_gate_contract(self):
        with patch.object(mod, 'assignment_audit', side_effect=ValueError('missing column')):
            with self.assertRaises(ValueError): mod.evaluate_bytes(RAW)

if __name__ == '__main__': unittest.main()
