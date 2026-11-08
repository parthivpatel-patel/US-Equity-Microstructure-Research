"""Characterization tests: demonstrate currently accepted invalid exchange sessions.

These tests document a known limitation; passing does not mean calendar validity.
Requires phase226 and its published phase224/225 dependencies on PYTHONPATH.
"""
import unittest
from phase226_matched_hac_bridge import matched_full_series_hac

class CalendarGapCharacterization(unittest.TestCase):
    def run_window(self, sessions):
        rows = [dict(date=d, security=s, exchange='X', hidden_count=h,
                     total_count=10)
                for d in sessions for s,h in [('T',2),('C',1)]]
        return matched_full_series_hac(rows, [('T','C')], sessions, ['X'],
                                       sessions[:2], sessions[2:], 0)

    def test_weekend_is_currently_accepted(self):
        dates = ['2025-09-05','2025-09-06','2025-09-07','2025-09-08']
        result = self.run_window(dates)
        self.assertEqual(result['early_n'], 2)
        self.assertFalse(result['calendar_authenticated'])

    def test_labor_day_is_currently_accepted(self):
        dates = ['2025-08-29','2025-09-01','2025-09-02','2025-09-03']
        result = self.run_window(dates)
        self.assertEqual(result['late_n'], 2)
        self.assertFalse(result['calendar_authenticated'])

    def test_valid_weekdays_are_also_accepted(self):
        dates = ['2025-09-02','2025-09-03','2025-09-04','2025-09-05']
        self.assertAlmostEqual(self.run_window(dates)['equal_cell_contrast']['difference'],0)

if __name__ == '__main__': unittest.main()
