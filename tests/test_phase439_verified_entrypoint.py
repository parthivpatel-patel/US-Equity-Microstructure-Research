"""Constructed-data integration contract tests; no historical SEC observations."""
import hashlib
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
for name in ('phase437_source_bound_gate', 'phase438_csv_integrity'):
    sys.modules[name] = types.ModuleType(name)
sys.modules['phase438_csv_integrity'].audit_bytes = lambda raw: {
    'source_sha256': hashlib.sha256(raw).hexdigest(), 'source_bytes': len(raw), 'structural_csv_valid': True}
def panel(raw):
    digest = hashlib.sha256(raw).hexdigest()
    return {'pass': True, 'source_sha256': digest, 'source_bytes': len(raw),
            'daily': {'source_sha256': digest, 'source_bytes': len(raw)},
            'calendar': {'source_sha256': digest, 'source_bytes': len(raw)}}
sys.modules['phase437_source_bound_gate'].evaluate_bytes = panel
from phase439_verified_entrypoint import evaluate_verified_bytes

class IntegrationContractTests(unittest.TestCase):
    def test_success_binds_all_fingerprints(self):
        result = evaluate_verified_bytes(b'constructed panel')
        self.assertTrue(result['structural_integrity']['structural_csv_valid'])
        self.assertFalse(result['historical_effect_estimated'])
    def test_structural_failure_prevents_panel_execution(self):
        with patch('phase439_verified_entrypoint.audit_bytes', side_effect=ValueError('bad header')):
            with patch('phase439_verified_entrypoint.evaluate_bytes') as downstream:
                with self.assertRaisesRegex(ValueError, 'bad header'):
                    evaluate_verified_bytes(b'bad')
                downstream.assert_not_called()
    def test_top_level_mismatch(self):
        with patch('phase439_verified_entrypoint.evaluate_bytes', return_value={'source_sha256':'wrong','source_bytes':3}):
            with self.assertRaisesRegex(ValueError, 'mismatch'):
                evaluate_verified_bytes(b'abc')
    def test_nested_digest_mismatch(self):
        broken = panel(b'abc'); broken['calendar']['source_sha256'] = 'wrong'
        with patch('phase439_verified_entrypoint.evaluate_bytes', return_value=broken):
            with self.assertRaisesRegex(ValueError, 'calendar'):
                evaluate_verified_bytes(b'abc')
    def test_nested_missing(self):
        broken = panel(b'abc'); del broken['daily']
        with patch('phase439_verified_entrypoint.evaluate_bytes', return_value=broken):
            with self.assertRaisesRegex(ValueError, 'daily'):
                evaluate_verified_bytes(b'abc')
    def test_nested_byte_length_mismatch(self):
        broken = panel(b'abc'); broken['daily']['source_bytes'] = 4
        with patch('phase439_verified_entrypoint.evaluate_bytes', return_value=broken):
            with self.assertRaisesRegex(ValueError, 'daily'):
                evaluate_verified_bytes(b'abc')

if __name__ == '__main__': unittest.main()
