import unittest
from scripts.phase329_cross_table_gate import audit

class Tests(unittest.TestCase):
    def setUp(self):
        self.s=[dict(outcome='count',pre_placebo_n='78',pre_placebo_at_least_as_negative='2',pre_placebo_at_least_as_extreme_absolute='2',nov_minus_oct_pp='-0.7346606598')]
        self.w=[dict(outcome='count',window_days='5',pre_placebo_count='78',pre_placebo_at_least_as_negative='2',pre_placebo_at_least_as_extreme_abs='2',nov_minus_oct_pp='-0.734661')]
    def test_match(self):
        self.assertTrue(all(audit(self.s,self.w)[0]['checks'].values()))
    def test_disagreement(self):
        self.w[0]['pre_placebo_at_least_as_extreme_abs']='3'
        self.assertFalse(audit(self.s,self.w)[0]['checks']['extreme_equal'])
    def test_missing(self):
        with self.assertRaises(ValueError):audit(self.s,[])
    def test_duplicate(self):
        with self.assertRaises(ValueError):audit(self.s,self.w*2)
    def test_sign_switch(self):
        self.w.append(dict(self.w[0],window_days='10',nov_minus_oct_pp='0.3'))
        self.assertTrue(audit(self.s,self.w)[0]['sign_sensitive'])

if __name__=='__main__':unittest.main()
