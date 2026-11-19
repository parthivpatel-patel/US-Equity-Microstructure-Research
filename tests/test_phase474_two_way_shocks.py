import unittest
from phase474_two_way_shocks import covariance, summary

class TwoWayTests(unittest.TestCase):
    def test_symmetry(self):
        c=covariance(40,(10,20,30),68)
        self.assertEqual(c[0][1],c[1][0])
    def test_group_shock_cancels(self):
        self.assertEqual(covariance(40,(10,20),10,group_loading=99),covariance(40,(10,20),10,group_loading=0))
    def test_no_date_shock_diversifies(self):
        a=covariance(40,(20,),10,date_loading=0)[0][0]
        b=covariance(40,(20,),20,date_loading=0)[0][0]
        self.assertAlmostEqual(a,2*b)
    def test_date_shock_does_not_diversify(self):
        a=covariance(40,(20,),10,noise_loading=0)[0][0]
        b=covariance(40,(20,),100,noise_loading=0)[0][0]
        self.assertAlmostEqual(a,b)
    def test_closed_form(self):
        self.assertAlmostEqual(covariance(40,(20,),68)[0][0],.1*(1+1/68))
    def test_inflation(self):
        self.assertAlmostEqual(summary()['se_inflation'][0],(69)**.5)
    def test_bad_cutoff(self):
        with self.assertRaises(ValueError): covariance(40,(0,),68)
    def test_bad_loading(self):
        with self.assertRaises(ValueError): covariance(40,(20,),68,date_loading=-1)

if __name__=='__main__': unittest.main()
