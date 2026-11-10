import unittest
from phase278_leave_exchange_out import leave_exchange_out

class TestLeaveExchangeOut(unittest.TestCase):
    def fixture(self):
        return {'pair_counts_by_exchange':{'X':2,'Y':1}, 'dates':[
            {'date':'2025-09-02','by_exchange':{'X':-2.,'Y':5.}},
            {'date':'2025-09-03','by_exchange':{'X':-2.,'Y':5.}}]}
    def test_weighting(self):
        r=leave_exchange_out(self.fixture())
        self.assertAlmostEqual(r['full_sample']['pair_weighted_mean'],1/3)
        self.assertAlmostEqual(r['full_sample']['exchange_equal_mean'],1.5)
    def test_leave_out(self):
        r=leave_exchange_out(self.fixture())
        self.assertEqual(r['leave_one_exchange_out']['X']['pair_weighted_mean'],5)
        self.assertEqual(r['leave_one_exchange_out']['Y']['pair_weighted_mean'],-2)
    def test_sign_reversal(self):
        r=leave_exchange_out(self.fixture())
        self.assertEqual(r['sign_reversals_pair_weighted'],['Y'])
        self.assertEqual(r['sign_reversals_exchange_equal'],['Y'])
    def test_one_exchange_rejected(self):
        d=self.fixture();d['pair_counts_by_exchange']={'X':2}
        with self.assertRaises(ValueError):leave_exchange_out(d)
    def test_missing_exchange_rejected(self):
        d=self.fixture();del d['dates'][0]['by_exchange']['Y']
        with self.assertRaises(ValueError):leave_exchange_out(d)
    def test_duplicate_date_rejected(self):
        d=self.fixture();d['dates'][1]['date']=d['dates'][0]['date']
        with self.assertRaises(ValueError):leave_exchange_out(d)
    def test_nonfinite_rejected(self):
        d=self.fixture();d['dates'][0]['by_exchange']['X']=float('nan')
        with self.assertRaises(ValueError):leave_exchange_out(d)
    def test_zero_count_rejected(self):
        d=self.fixture();d['pair_counts_by_exchange']['X']=0
        with self.assertRaises(ValueError):leave_exchange_out(d)
    def test_no_dates_rejected(self):
        d=self.fixture();d['dates']=[]
        with self.assertRaises(ValueError):leave_exchange_out(d)
    def test_no_historical_authorization(self):
        self.assertFalse(leave_exchange_out(self.fixture())['historical_inference_authorized'])

if __name__=='__main__':unittest.main()
