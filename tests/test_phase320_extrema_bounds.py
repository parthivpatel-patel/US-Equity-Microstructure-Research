"""Synthetic and published-summary checks for Phase 320."""
import unittest
from scripts.phase320_extrema_bounds import bounds

class TestExtremaBounds(unittest.TestCase):
    def test_published_count(self):
        self.assertEqual(bounds("-0.7346606598677254",78,2,2,"-1.4475738789418606","1.0538523294152946"),(76,77))
    def test_published_volume(self):
        self.assertEqual(bounds("0.626597999820323",78,48,76,"-1.8665501312689659","1.4840122108986915"),(28,75))
    def test_negative_tie(self):
        self.assertEqual(bounds(-1,4,2,2,-1,2),(2,4))
    def test_positive_no_negative_extreme(self):
        self.assertEqual(bounds(1,4,2,2,-0.5,2),(0,2))
    def test_invalid(self):
        with self.assertRaises(ValueError):
            bounds(1,4,5,2,-2,2)
if __name__ == "__main__":
    unittest.main()
