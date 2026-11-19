import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from phase479_missingness import contrast_variance,example
class TestMissingness(unittest.TestCase):
 def test_balanced_factor_cancels(self):
  a,_=example(); self.assertAlmostEqual(a['factor_variance'],0,places=12)
 def test_missingness_breaks_cancellation(self):
  _,b=example(); self.assertGreater(b['factor_variance'],0)
 def test_identical_loadings_cancel_within_date(self):
  a=contrast_variance([.5,.5],[[True]*40]*2)
  self.assertAlmostEqual(a['factor_variance'],.25*contrast_variance([1.0],[[True]*40])['factor_variance'])
 def test_invariance_to_weight_scaling(self):
  a=contrast_variance([.5,-.5],[[True]*40]*2,[1,3]);b=contrast_variance([.5,-.5],[[True]*40]*2,[2,6]);self.assertAlmostEqual(a['total_variance'],b['total_variance'])
 def test_empty_date_rejected(self):
  with self.assertRaises(ValueError):contrast_variance([.5],[[True]*39+[False]])
 def test_zero_factor_when_no_loadings(self):
  a=contrast_variance([0,0],[[True]*40]*2);self.assertAlmostEqual(a['factor_variance'],0)
if __name__=='__main__':unittest.main()
