"""Phase 355 metamorphic tests: constructed fixtures only, never SEC data."""
import unittest
from scripts.phase352_calendar_serial import calendar_serial_components as calc

DATES = ['2025-10-01', '2025-10-02', '2025-10-03', '2025-10-06']
ROWS = [('a', DATES[0], 1.), ('a', DATES[2], 5.),
        ('b', DATES[0], 3.), ('b', DATES[2], 7.)]

class CalendarProperties(unittest.TestCase):
    def test_row_permutation_invariance(self):
        a, b = calc(ROWS, DATES, 2), calc(list(reversed(ROWS)), DATES, 2)
        for key in ('mean_pp', 'group_component', 'date_component',
                    'intersection_component', 'serial_date_component',
                    'two_way_raw_variance', 'serial_adjusted_raw_variance'):
            self.assertAlmostEqual(a[key], b[key], places=12)

    def test_zero_lag_equals_date_component(self):
        a = calc(ROWS, DATES, 0)
        self.assertEqual(a['lag_products'], [a['date_component']])
        self.assertEqual(a['serial_date_component'], a['date_component'])
        self.assertEqual(a['serial_adjusted_raw_variance'], a['two_way_raw_variance'])

    def test_missing_sessions_are_explicit(self):
        a = calc(ROWS, DATES, 2)
        self.assertEqual(a['missing_sessions'], [DATES[1], DATES[3]])
        self.assertEqual(a['lag_products'][1], 0.)

    def test_lag_cap_at_calendar_length(self):
        a = calc(ROWS, DATES, 100)
        self.assertEqual(len(a['lag_products']), len(DATES))

    def test_reject_duplicate_session(self):
        with self.assertRaisesRegex(ValueError, 'invalid calendar'):
            calc(ROWS, DATES[:2] + [DATES[1]] + DATES[2:])

    def test_reject_boolean_lag(self):
        with self.assertRaisesRegex(ValueError, 'invalid lag'):
            calc(ROWS, DATES, True)

if __name__ == '__main__':
    unittest.main()
