import unittest
from scripts.phase299_numeric_admission import finite_float

class NumericAdmissionTests(unittest.TestCase):
    def test_normal(self):
        self.assertEqual(finite_float(3), 3.0)
    def test_extreme_integer(self):
        for value in (10**1000, -(10**1000)):
            with self.subTest(value=str(value)[:5]), self.assertRaises(ValueError):
                finite_float(value)
    def test_nonfinite(self):
        for value in (float('inf'), float('-inf'), float('nan')):
            with self.assertRaises(ValueError): finite_float(value)
    def test_bool_rejected(self):
        with self.assertRaises(ValueError): finite_float(True)
    def test_positive(self):
        self.assertEqual(finite_float(5e-324, positive=True), 5e-324)
        for value in (0, -1):
            with self.assertRaises(ValueError): finite_float(value, positive=True)
    def test_other_types(self):
        for value in ('1', None, 1+0j):
            with self.assertRaises(ValueError): finite_float(value)

if __name__ == '__main__': unittest.main()
