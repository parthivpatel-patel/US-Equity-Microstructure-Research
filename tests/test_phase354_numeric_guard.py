"""Constructed-data numeric-stability regression checks, not SEC estimates."""
import unittest
from scripts.phase352_calendar_serial import calendar_serial_components as calc

S = ['2025-10-01', '2025-10-02', '2025-10-03']

class NumericGuardTests(unittest.TestCase):
    def test_extreme_finite_inputs_do_not_emit_nan(self):
        rows = [('a', S[0], 1e308), ('a', S[1], -1e308),
                ('b', S[0], 1e308), ('b', S[1], -1e308)]
        with self.assertRaisesRegex(ValueError, 'nonfinite covariance'):
            calc(rows, S)

    def test_finite_regular_fixture(self):
        rows = [('a', S[0], 1.), ('a', S[2], 5.),
                ('b', S[0], 3.), ('b', S[2], 7.)]
        result = calc(rows, S, 1)
        self.assertAlmostEqual(result['mean_pp'], 4.)
        self.assertAlmostEqual(result['lag_products'][0], 2.)
        self.assertAlmostEqual(result['lag_products'][1], 0.)

    def test_nonfinite_input_rejected(self):
        rows = [('a', S[0], float('inf')), ('a', S[1], 2.),
                ('b', S[0], 3.), ('b', S[1], 4.)]
        with self.assertRaisesRegex(ValueError, 'invalid contrast'):
            calc(rows, S)

    def test_invalid_date_rejected(self):
        rows = [('a', '2025-10-04', 1.), ('a', S[1], 2.),
                ('b', S[0], 3.), ('b', S[1], 4.)]
        with self.assertRaisesRegex(ValueError, 'off-calendar'):
            calc(rows, S)

if __name__ == '__main__':
    unittest.main()
