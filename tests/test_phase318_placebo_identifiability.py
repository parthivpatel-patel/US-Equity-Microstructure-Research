import unittest
from scripts.phase318_placebo_identifiability import bounds


class BoundsTest(unittest.TestCase):
    def test_published_count(self):
        b = bounds('-0.7346606598677254', 78, 2, 2)
        self.assertEqual((76, 78), (b['right_tail_min'], b['right_tail_max']))

    def test_published_volume(self):
        b = bounds('0.626597999820323', 78, 48, 76)
        self.assertEqual((28, 76), (b['right_tail_min'], b['right_tail_max']))

    def test_positive_zero_absolute(self):
        self.assertEqual(0, bounds('1', 10, 5, 0)['right_tail_max'])

    def test_negative_inconsistent(self):
        with self.assertRaises(ValueError):
            bounds('-1', 10, 7, 6)

    def test_invalid(self):
        for x in ('NaN', '0'):
            with self.assertRaises(ValueError):
                bounds(x, 10, 2, 4)


if __name__ == '__main__':
    unittest.main()
