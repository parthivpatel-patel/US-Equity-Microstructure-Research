"""Deterministic checks for Phase 328 necessary aggregate conditions."""
import unittest
from scripts.phase328_aggregate_feasibility import audit

def row(d='-0.7',lo='-1.4',hi='1.1',negative='2',extreme='2',n='78'):
    return {'outcome':'count','nov_minus_oct_pp':d,'pre_placebo_min_pp':lo,
            'pre_placebo_max_pp':hi,'pre_placebo_at_least_as_negative':negative,
            'pre_placebo_at_least_as_extreme_absolute':extreme,'pre_placebo_n':n}

class Phase328Tests(unittest.TestCase):
    def test_count_contradiction(self):
        r=audit(row()); self.assertEqual(r['necessary_minimum'],3); self.assertFalse(r['consistent_with_necessary_conditions'])
    def test_repaired_count(self):
        self.assertTrue(audit(row(extreme='3'))['consistent_with_necessary_conditions'])
    def test_volume_like(self):
        self.assertTrue(audit(row(d='0.6',negative='48',extreme='76'))['consistent_with_necessary_conditions'])
    def test_zero_event(self):
        self.assertFalse(audit(row(d='0',extreme='77'))['consistent_with_necessary_conditions'])
    def test_invalid_n(self):
        with self.assertRaises(ValueError): audit(row(n='0'))
    def test_nonfinite(self):
        with self.assertRaises(ValueError): audit(row(d='NaN'))
    def test_outside_range(self):
        self.assertFalse(audit(row(d='-2',negative='2'))['consistent_with_necessary_conditions'])

if __name__=='__main__':
    unittest.main()
