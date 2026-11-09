import unittest
from scripts.phase274_pretrend import evaluate

CAL = ['2025-09-02','2025-09-03','2025-09-05','2025-09-08']
EARLY = ('2025-09-02','2025-09-03')
LATE = ('2025-09-05','2025-09-08')
ROWS = list(zip(CAL,[0.,1.,3.,6.]))

def run(cal=CAL, rows=ROWS, early=EARLY, late=LATE):
    return evaluate(cal,rows,early,late)

class Tests(unittest.TestCase):
    def test_calendar_day_slope(self):
        r=run(); self.assertAlmostEqual(r['early']['slope_per_calendar_day'],1); self.assertAlmostEqual(r['late']['slope_per_calendar_day'],1)
    def test_mean_difference(self): self.assertAlmostEqual(run()['late_minus_early_mean'],4)
    def test_authentication_not_inferred(self): self.assertFalse(run()['causal_inference_authorized'])
    def test_missing(self):
        with self.assertRaises(ValueError): run(rows=ROWS[:-1])
    def test_extra(self):
        with self.assertRaises(ValueError): run(rows=ROWS+[('2025-09-09',1)])
    def test_duplicate(self):
        with self.assertRaises(ValueError): run(rows=ROWS[:-1]+[ROWS[0]])
    def test_nan(self):
        with self.assertRaises(ValueError): run(rows=ROWS[:-1]+[(CAL[-1],float('nan'))])
    def test_calendar_unsorted(self):
        with self.assertRaises(ValueError): run(cal=CAL[::-1])
    def test_overlapping_windows(self):
        with self.assertRaises(ValueError): run(late=('2025-09-03','2025-09-08'))
    def test_single_session_window(self):
        with self.assertRaises(ValueError): run(early=('2025-09-02','2025-09-02'))
    def test_outcome_bool(self):
        with self.assertRaises(ValueError): run(rows=ROWS[:-1]+[(CAL[-1],True)])
    def test_irregular_dates(self):
        r=run(rows=list(zip(CAL,[0,1,3,6]))); self.assertAlmostEqual(r['late']['slope_per_calendar_day'],1)

if __name__=='__main__': unittest.main()
