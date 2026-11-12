import unittest
from scripts.phase319_placebo_sharp_bounds import right_tail_bounds

class SharpBoundsTests(unittest.TestCase):
    def test_published_count(self):
        self.assertEqual(right_tail_bounds('-0.7346606598677254',78,2,2),(76,78))
    def test_published_volume_conditional(self):
        self.assertEqual(right_tail_bounds('0.626597999820323',78,48,76,no_ties=True),(28,30))
    def test_published_volume_unconditional(self):
        self.assertEqual(right_tail_bounds('0.626597999820323',78,48,76),(28,76))
    def test_positive_all_lower(self):
        self.assertEqual(right_tail_bounds('1',5,5,3,no_ties=True),(0,0))
    def test_positive_all_absolute(self):
        self.assertEqual(right_tail_bounds('1',5,2,5,no_ties=True),(3,3))
    def test_negative_invalid(self):
        with self.assertRaises(ValueError): right_tail_bounds('-1',5,4,3)
    def test_bool_rejected(self):
        with self.assertRaises(ValueError): right_tail_bounds('1',5,True,3)
    def test_nonfinite_rejected(self):
        with self.assertRaises(ValueError): right_tail_bounds('NaN',5,2,3)
    def test_positive_zero_lower(self):
        self.assertEqual(right_tail_bounds('1',5,0,4,no_ties=True),(4,4))
