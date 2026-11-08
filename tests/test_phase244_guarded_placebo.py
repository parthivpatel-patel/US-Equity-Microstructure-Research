"""Synthetic integration tests for guarded descriptive placebo scan."""
import unittest
from phase244_guarded_placebo import guarded_placebo_scan

DATES = ['2025-09-29','2025-09-30','2025-10-01','2025-10-02','2025-10-03','2025-10-06']

def rows(dates=DATES):
    return [dict(date=d, equal_cell_contrast=float(i), pooled_count_contrast=float(2*i)) for i,d in enumerate(dates)]

class GuardedPlaceboTests(unittest.TestCase):
    def test_valid_numeric(self):
        out=guarded_placebo_scan(rows(), [3], 3, 1, admitted_sessions=DATES)
        self.assertAlmostEqual(out['results'][0]['equal_cell_difference'], 3.0)
        self.assertAlmostEqual(out['results'][0]['pooled_count_difference'], 6.0)
        self.assertFalse(out['calendar_independently_verified'])
        self.assertTrue(out['session_roster_supplied'])
    def test_weekend_rejected(self):
        dates=DATES.copy(); dates[4]='2025-10-04'
        with self.assertRaises(ValueError): guarded_placebo_scan(rows(dates), [3], 3, 1)
    def test_holiday_not_authenticated(self):
        dates=DATES.copy(); dates[0]='2025-09-01'
        out=guarded_placebo_scan(rows(dates), [3], 3, 1)
        self.assertFalse(out['calendar_independently_verified'])
    def test_roster_mismatch(self):
        with self.assertRaises(ValueError): guarded_placebo_scan(rows(), [3], 3, 1, admitted_sessions=DATES[:-1])
    def test_duplicate_rejected(self):
        dates=DATES.copy(); dates[1]=dates[0]
        with self.assertRaises(ValueError): guarded_placebo_scan(rows(dates), [3], 3, 1)
    def test_incomplete_window(self):
        with self.assertRaises(ValueError): guarded_placebo_scan(rows(), [2], 3, 1)
    def test_invalid_numeric(self):
        data=rows(); data[1]['equal_cell_contrast']=float('nan')
        with self.assertRaises(ValueError): guarded_placebo_scan(data, [3], 3, 1)

if __name__ == '__main__': unittest.main()
