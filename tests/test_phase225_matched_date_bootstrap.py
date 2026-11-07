import unittest
from scripts.phase225_matched_date_bootstrap import matched_daily,circular_block_window_bootstrap
D=['2025-09-29','2025-09-30','2025-10-01','2025-10-02']
P=[('T','C')]
E=['X','Y']
def panel():
    return [{'date':d,'security':s,'exchange':e,'hidden_count':(2+i if s=='T' else 1+i),'total_count':10} for i,d in enumerate(D) for s in ('T','C') for e in E]
class TestMatched(unittest.TestCase):
    def test_expected_daily(self): self.assertEqual([round(x['matched_contrast'],8) for x in matched_daily(panel(),P,D,E)],[.1]*4)
    def test_duplicate_rejected(self):
        with self.assertRaises(ValueError): matched_daily(panel()+panel()[:1],P,D,E)
    def test_missing_rejected(self):
        with self.assertRaises(ValueError): matched_daily(panel()[:-1],P,D,E)
    def test_overlapping_pairs(self):
        with self.assertRaises(ValueError): matched_daily(panel(),[('T','C'),('C','T')],D,E)
    def test_reform_boundary(self):
        with self.assertRaises(ValueError): matched_daily(panel(),P,D+['2025-11-03'],E)
    def test_reproducible_bootstrap(self):
        daily=[{'date':d,'matched_contrast':v} for d,v in zip(D,[0,.2,.4,.8])]
        x=circular_block_window_bootstrap(daily,D[:2],D[2:],2,100,123)
        self.assertEqual(x,circular_block_window_bootstrap(daily,D[:2],D[2:],2,100,123))
        self.assertAlmostEqual(x['observed_difference'],.5)
    def test_constant_bootstrap(self):
        x=circular_block_window_bootstrap(matched_daily(panel(),P,D,E),D[:2],D[2:],1,20)
        self.assertAlmostEqual(x['observed_difference'],0)
        self.assertAlmostEqual(x['percentile_025'],0)
    def test_block_too_long(self):
        with self.assertRaises(ValueError): circular_block_window_bootstrap(matched_daily(panel(),P,D,E),D[:2],D[2:],3,20)
if __name__=='__main__': unittest.main()
