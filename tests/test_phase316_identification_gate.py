"""Deterministic synthetic fixtures only; not SEC observation tests."""
import tempfile
import unittest
from pathlib import Path
from scripts.phase316_identification_gate import audit

SUMMARY = '''outcome,nov_minus_oct_pp,pre_placebo_n,pre_placebo_at_least_as_negative,pre_placebo_at_least_as_extreme_absolute,pre_placebo_min_pp,pre_placebo_max_pp
count,-0.7,78,2,2,-1.5,1.1
volume,0.6,78,48,76,-1.9,1.5
'''
GROUPS = '''outcome,group_bootstrap_ci_low,group_bootstrap_ci_high,leave_one_group_out_min,leave_one_group_out_max
count,-2,0.5,-0.9,-0.3
volume,-1,2,0.3,0.8
'''

class GateTests(unittest.TestCase):
    def check(self, s=SUMMARY, g=GROUPS):
        with tempfile.TemporaryDirectory() as temp:
            a, b = Path(temp)/'summary.csv', Path(temp)/'groups.csv'
            a.write_text(s, encoding='utf-8')
            b.write_text(g, encoding='utf-8')
            return audit(a, b)

    def test_frozen_pattern(self):
        out = self.check()
        self.assertTrue(all(r['bootstrap_includes_zero'] for r in out.values()))
        self.assertTrue(all(r['leave_one_group_out_same_sign'] for r in out.values()))

    def test_duplicate_outcome_rejected(self):
        with self.assertRaisesRegex(ValueError, 'exactly one'):
            self.check(s=SUMMARY + SUMMARY.splitlines()[-1] + '\n')

    def test_bad_frequency_rejected(self):
        with self.assertRaisesRegex(ValueError, 'invalid placebo'):
            self.check(s=SUMMARY.replace('78,2,2', '78,2,79'))

    def test_bad_placebo_range_rejected(self):
        with self.assertRaisesRegex(ValueError, 'outside placebo'):
            self.check(s=SUMMARY.replace('-1.5,1.1', '-0.5,1.1'))

    def test_bad_leave_one_out_range_rejected(self):
        with self.assertRaisesRegex(ValueError, 'invalid group'):
            self.check(g=GROUPS.replace('-0.9,-0.3', '-0.2,0.1'))

    def test_sign_flip_rejected(self):
        with self.assertRaisesRegex(ValueError, 'invalid group sensitivity range'):
            self.check(s=SUMMARY.replace('volume,0.6', 'volume,-0.6'))

if __name__ == '__main__':
    unittest.main()
