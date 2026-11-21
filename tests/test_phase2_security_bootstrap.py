import importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/'scripts'/'phase2_security_bootstrap.py'
s=importlib.util.spec_from_file_location('audit',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class TestBootstrap(unittest.TestCase):
 def setUp(self):
  self.a={1:[('a',{'dr':.1,'dv':.2,'trades_pre':10}),('b',{'dr':.2,'dv':.3,'trades_pre':20})],0:[('c',{'dr':0.,'dv':.1,'trades_pre':10}),('d',{'dr':0.,'dv':.1,'trades_pre':20})]}
 def test_equal(self):self.assertAlmostEqual(m.gap(self.a[1],self.a[0],'dr'),15)
 def test_weighted(self):self.assertAlmostEqual(m.gap(self.a[1],self.a[0],'dr',True),100*5/30)
 def test_quantile(self):self.assertAlmostEqual(m.quantile([1,2,3,4],.25),1.75)
 def test_reproducible(self):self.assertEqual(m.analyze(self.a,100,7),m.analyze(self.a,100,7))
 def test_seed(self):self.assertNotEqual(m.analyze(self.a,100,7),m.analyze(self.a,100,8))
 def test_low_n(self):
  with self.assertRaises(ValueError):m.analyze(self.a,99)
 def test_leave_one_out(self):self.assertAlmostEqual(m.analyze(self.a,100)['estimands']['hidden_trade_equal_security']['largest_treated_leave_one_out_shift_abs_pp'],5)
if __name__=='__main__':unittest.main()
