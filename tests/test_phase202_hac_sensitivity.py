import unittest
from math import isclose
from phase202_hac_sensitivity import lag_sensitivity

ROWS = [{"date":d,"contrast":x} for d,x in zip(["2025-10-01","2025-10-02","2025-10-03","2025-10-06"],[1,2,3,4])]
class TestSensitivity(unittest.TestCase):
    def test_known_values(self):
        r=lag_sensitivity(ROWS,(0,1))
        self.assertEqual(r['mean'],2.5)
        self.assertTrue(isclose(r['sensitivity'][0]['hac_se'],(1.25/4)**.5))
        self.assertTrue(isclose(r['sensitivity'][1]['hac_se'],.625))
    def test_all_lags_same_mean(self):
        self.assertEqual(len(lag_sensitivity(ROWS,(0,1,2,3))['sensitivity']),4)
    def test_empty(self):
        with self.assertRaises(ValueError): lag_sensitivity([])
    def test_duplicate_date(self):
        with self.assertRaises(ValueError): lag_sensitivity([ROWS[0],ROWS[0]])
    def test_unsorted(self):
        with self.assertRaises(ValueError): lag_sensitivity(ROWS[::-1])
    def test_nonfinite(self):
        with self.assertRaises(ValueError): lag_sensitivity([ROWS[0],dict(ROWS[1],contrast=float('nan'))])
    def test_invalid_lags(self):
        for lags in [(),(-1,),(4,),(True,),(1,1)]:
            with self.subTest(lags=lags),self.assertRaises(ValueError): lag_sensitivity(ROWS,lags)
    def test_noncanonical_date(self):
        with self.assertRaises(ValueError): lag_sensitivity([dict(ROWS[0],date='2025-1-1'),ROWS[1]])
    def test_gapped_dates_not_rejected(self):
        self.assertEqual(lag_sensitivity(ROWS,(1,))['lag_units'],'observed_sessions')
if __name__ == '__main__': unittest.main()
