"""Integration checks using actual repository dependency interfaces."""
import unittest
from phase247_overlap_guarded_scan import overlap_guarded_placebo_scan


def fixture():
    # Weekdays only; intentionally not represented as an authenticated exchange calendar.
    from datetime import date, timedelta
    d = date(2025, 9, 2)
    dates = []
    while len(dates) < 14:
        if d.weekday() < 5:
            dates.append(d.isoformat())
        d += timedelta(days=1)
    return [{'date': day, 'equal_cell_contrast': float(i),
             'pooled_count_contrast': float(2*i)} for i, day in enumerate(dates)]


class Integration(unittest.TestCase):
    def test_overlapping_cuts_and_estimands(self):
        rows = fixture()
        result = overlap_guarded_placebo_scan(rows, [4, 5, 6], 3, 0)
        self.assertEqual(result['overlap_audit']['n_overlapping_pairs'], 3)
        self.assertEqual([p['shared_sessions'] for p in result['overlap_audit']['overlapping_pairs']], [5, 4, 5])
        self.assertEqual([x['equal_cell_difference'] for x in result['results']], [3.0]*3)
        self.assertEqual([x['pooled_count_difference'] for x in result['results']], [6.0]*3)
        for key in ('source_authenticated', 'treatment_authenticated', 'calendar_independently_verified', 'causal_effect_established', 'multiplicity_adjusted', 'serial_dependence_fully_addressed'):
            self.assertFalse(result[key])

    def test_nonoverlap_does_not_assert_independence(self):
        result = overlap_guarded_placebo_scan(fixture(), [3, 9], 3, 0)
        self.assertEqual(result['overlap_audit']['n_overlapping_pairs'], 0)
        self.assertFalse(result['serial_dependence_fully_addressed'])

    def test_rejects_weekend(self):
        rows = fixture()
        rows[0]['date'] = '2025-08-31'
        with self.assertRaises(ValueError):
            overlap_guarded_placebo_scan(rows, [4], 3, 0)

    def test_rejects_mismatched_roster(self):
        with self.assertRaises(ValueError):
            overlap_guarded_placebo_scan(fixture(), [4], 3, 0, admitted_sessions=['2025-09-02'])

    def test_rejects_bad_bandwidth(self):
        with self.assertRaises(ValueError):
            overlap_guarded_placebo_scan(fixture(), [4], 3, 6)

    def test_rejects_incomplete_window(self):
        with self.assertRaises(ValueError):
            overlap_guarded_placebo_scan(fixture(), [2], 3, 0)


if __name__ == '__main__':
    unittest.main()
