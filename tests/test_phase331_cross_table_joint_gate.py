"""Deterministic aggregate-only tests. No underlying SEC records are used."""
import unittest
from scripts.phase331_cross_table_joint_gate import audit

class TestGate(unittest.TestCase):
    def setUp(self):
        self.s=[dict(outcome='count',nov_minus_oct_pp='-0.7346606598677254',
            pre_placebo_min_pp='-1.4475738789418606',
            pre_placebo_max_pp='1.0538523294152946',pre_placebo_n='78',
            pre_placebo_at_least_as_negative='2',
            pre_placebo_at_least_as_extreme_absolute='2')]
        self.w=[dict(outcome='count',window_days='5',nov_minus_oct_pp='-0.734661',
            pre_placebo_count='78',pre_placebo_at_least_as_negative='2',
            pre_placebo_at_least_as_extreme_abs='2')]
    def test_contradiction(self):
        self.assertFalse(audit(self.s,self.w)[0]['joint_feasible_necessary_condition'])
    def test_minimum_three(self):
        self.assertEqual(audit(self.s,self.w)[0]['required_absolute_extremes_lower_bound'],3)
    def test_repaired_count(self):
        self.s[0]['pre_placebo_at_least_as_extreme_absolute']='3'
        self.w[0]['pre_placebo_at_least_as_extreme_abs']='3'
        self.assertTrue(audit(self.s,self.w)[0]['joint_feasible_necessary_condition'])
    def test_lineage_mismatch(self):
        self.w[0]['pre_placebo_count']='77'
        self.assertFalse(audit(self.s,self.w)[0]['five_day_tail_counts_match'])
    def test_duplicate_rejected(self):
        with self.assertRaises(ValueError): audit(self.s,self.w+self.w)
    def test_missing_rejected(self):
        with self.assertRaises(ValueError): audit(self.s,[])
    def test_positive_minimum(self):
        self.s[0].update(nov_minus_oct_pp='0.5',pre_placebo_min_pp='-0.8',
            pre_placebo_max_pp='0.9',pre_placebo_at_least_as_negative='0',
            pre_placebo_at_least_as_extreme_absolute='1')
        self.w[0].update(nov_minus_oct_pp='0.5',
            pre_placebo_at_least_as_negative='0',
            pre_placebo_at_least_as_extreme_abs='1')
        self.assertEqual(audit(self.s,self.w)[0]['required_absolute_extremes_lower_bound'],1)

if __name__=='__main__': unittest.main()
