import unittest
from decimal import Decimal
from scripts.phase330_arithmetic_gate import check

class TestGate(unittest.TestCase):
    def row(self, **changes):
        row=dict(outcome='count',window_days='5',november_pp='-1.335781',october6_pp='-0.601120',nov_minus_oct_pp='-0.734661',pre_placebo_count='78',pre_placebo_at_least_as_negative='2',pre_placebo_at_least_as_extreme_abs='2')
        row.update(changes)
        return row
    def test_valid(self): self.assertTrue(check([], [self.row()])[0]['arithmetic_ok'])
    def test_mismatch(self): self.assertFalse(check([], [self.row(nov_minus_oct_pp='1')])[0]['arithmetic_ok'])
    def test_duplicates(self):
        with self.assertRaises(ValueError): check([], [self.row(),self.row()])
    def test_nonfinite(self):
        with self.assertRaises(ValueError): check([], [self.row(november_pp='NaN')])
    def test_negative_subset(self): self.assertFalse(check([], [self.row(pre_placebo_at_least_as_negative='3')])[0]['negative_tail_subset_ok'])
    def test_positive_subset_not_required(self): self.assertTrue(check([], [self.row(nov_minus_oct_pp='1',pre_placebo_at_least_as_negative='3')])[0]['negative_tail_subset_ok'])
    def test_invalid_count(self):
        with self.assertRaises(ValueError): check([], [self.row(pre_placebo_count='-1')])
    def test_tolerance(self): self.assertTrue(check([], [self.row(nov_minus_oct_pp='-0.734662')],Decimal('0.0000015'))[0]['arithmetic_ok'])

if __name__=='__main__': unittest.main()
