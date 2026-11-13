import unittest
from phase342_matched_contrasts import analyze

def row(s,d,ex,t,g,n,den=100):
    return dict(security=s,date=d,exchange=ex,treated=t,match_group=g,numerator=str(n),denominator=str(den))

class Tests(unittest.TestCase):
    def test_pair(self):
        r=analyze([row('a','2025-10-01','X','1','g',30),row('b','2025-10-01','X','0','g',10)])
        self.assertAlmostEqual(r['equal_group_mean_difference_pp'],20)
    def test_exchange_disjoint(self):
        r=analyze([row('a','2025-10-01','X','1','g',30),row('b','2025-10-01','Y','0','g',10)])
        self.assertIsNone(r['equal_group_mean_difference_pp'])
        self.assertEqual(r['unpaired_strata'],2)
    def test_ratio_of_sums(self):
        r=analyze([row('a','2025-10-01','X','1','g',1,10),row('c','2025-10-01','X','1','g',90,100),row('b','2025-10-01','X','0','g',0)])
        self.assertAlmostEqual(r['equal_group_mean_difference_pp'],100*91/110)
    def test_group_weight(self):
        data=[row('a','2025-10-01','X','1','g1',30),row('b','2025-10-01','X','0','g1',10),row('c','2025-10-01','X','1','g2',10),row('d','2025-10-01','X','0','g2',10),row('a','2025-10-02','X','1','g1',30),row('b','2025-10-02','X','0','g1',10)]
        self.assertAlmostEqual(analyze(data)['equal_group_mean_difference_pp'],10)
    def test_duplicate(self):
        a=row('a','2025-10-01','X','1','g',10)
        with self.assertRaisesRegex(ValueError,'duplicate'): analyze([a,a])
    def test_drift(self):
        with self.assertRaisesRegex(ValueError,'drift'): analyze([row('a','2025-10-01','X','1','g',10),row('a','2025-10-02','X','0','g',10)])
    def test_excess_numerator(self):
        with self.assertRaisesRegex(ValueError,'invalid numerator'): analyze([row('a','2025-10-01','X','1','g',101)])
    def test_zero_denominator(self):
        with self.assertRaisesRegex(ValueError,'invalid numerator'): analyze([row('a','2025-10-01','X','1','g',0,0)])
    def test_empty(self):
        with self.assertRaisesRegex(ValueError,'empty'): analyze([])
    def test_bad_date(self):
        with self.assertRaisesRegex(ValueError,'invalid date'): analyze([row('a','2025-02-30','X','1','g',1)])

if __name__=='__main__': unittest.main()
