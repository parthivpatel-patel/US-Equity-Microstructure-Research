import unittest
from phase286_hac_inference_gate import assess_hac

BASE = dict(n_dates=40, lag=2, weighting='pair', mean=0.1,
            hac_standard_error=0.02, source_authenticated=False,
            causal_inference_authorized=False)

class GateTests(unittest.TestCase):
    def test_admitted(self):
        self.assertTrue(assess_hac(BASE)['descriptive_inference_admissible'])
    def test_zero_se(self):
        self.assertIn('zero_or_near_zero_standard_error', assess_hac({**BASE, 'hac_standard_error':0})['reasons'])
    def test_near_zero_se(self):
        self.assertFalse(assess_hac({**BASE, 'hac_standard_error':1e-13})['descriptive_inference_admissible'])
    def test_short(self):
        self.assertIn('short_common_date_sample', assess_hac({**BASE,'n_dates':10})['reasons'])
    def test_lag(self):
        self.assertIn('large_hac_lag_relative_to_sample', assess_hac({**BASE,'lag':15})['reasons'])
    def test_multiple_reasons(self):
        self.assertEqual(len(assess_hac({**BASE,'n_dates':10,'lag':5,'hac_standard_error':0})['reasons']),3)
    def test_invalid_provenance(self):
        for flag in (True, None):
            with self.subTest(flag=flag), self.assertRaises(ValueError):
                assess_hac({**BASE,'source_authenticated':flag})
    def test_invalid_numbers(self):
        for k,v in [('mean',float('nan')),('hac_standard_error',-1),('n_dates',True),('lag',-1)]:
            with self.subTest(k=k), self.assertRaises(ValueError):
                assess_hac({**BASE,k:v})
    def test_invalid_configuration(self):
        for kwargs in ({'min_dates':1},{'max_lag_fraction':float('nan')},{'se_floor':0}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                assess_hac(BASE,**kwargs)
    def test_exchange_weighting(self):
        self.assertEqual(assess_hac({**BASE,'weighting':'exchange'})['weighting'],'exchange')
    def test_no_p_value(self):
        self.assertNotIn('p_value',assess_hac(BASE))

if __name__ == '__main__': unittest.main()
