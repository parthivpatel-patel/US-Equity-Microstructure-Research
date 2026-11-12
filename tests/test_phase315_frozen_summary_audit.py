"""Deterministic tests for Phase 315 frozen-summary audit."""
import tempfile
import unittest
from pathlib import Path
from scripts.phase315_frozen_summary_audit import audit

S = 'outcome,november_pp,october_pp,nov_minus_oct_pp,pre_placebo_n,pre_placebo_at_least_as_negative,pre_placebo_at_least_as_extreme_absolute\ncount,-1.3,-0.6,-0.7,78,2,2\nvolume,-0.1,-0.6,0.5,78,48,76\n'
G = 'outcome,difference_pp,group_bootstrap_ci_low,group_bootstrap_ci_high\ncount,-0.7,-2,0.5\nvolume,0.5,-1,2\n'

class AuditTests(unittest.TestCase):
    def run_case(self, summary=S, groups=G):
        with tempfile.TemporaryDirectory() as d:
            a, b = Path(d)/'a.csv', Path(d)/'b.csv'
            a.write_text(summary); b.write_text(groups)
            return audit(a, b)

    def test_valid(self):
        r = self.run_case()
        self.assertTrue(all(x['ci_includes_zero'] for x in r.values()))
        self.assertEqual(r['count']['descriptive_extreme_fraction'], '2/78')

    def test_arithmetic_reject(self):
        with self.assertRaisesRegex(ValueError, 'difference inconsistency'):
            self.run_case(S.replace(',-0.7,78', ',-0.8,78'))

    def test_invalid_placebo_count(self):
        with self.assertRaisesRegex(ValueError, 'invalid placebo counts'):
            self.run_case(S.replace(',78,2,2', ',78,2,79'))

    def test_interval_reject(self):
        with self.assertRaisesRegex(ValueError, 'inconsistent interval'):
            self.run_case(groups=G.replace(',-2,0.5', ',0.2,0.5'))

    def test_missing_outcome(self):
        with self.assertRaisesRegex(ValueError, 'unexpected outcome keys'):
            self.run_case(groups=G.split('volume,')[0])

if __name__ == '__main__':
    unittest.main()
