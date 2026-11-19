import unittest
from phase475_heterogeneous_date import covariance,weights
class Tests(unittest.TestCase):
 def test_weights(self): self.assertAlmostEqual(sum(weights(40,20)),0)
 def test_cancel(self): self.assertEqual(covariance(40,[20],68,1,1,.5,0),covariance(40,[20],68,0,1,.5,1))
 def test_symmetry(self):
  m=covariance(40,[10,20,30],68,1,1,.5,.5)
  self.assertAlmostEqual(m[0][1],m[1][0])
 def test_idio(self): self.assertAlmostEqual(covariance(40,[20],68,0,1,0,0)[0][0],.2/68)
 def test_scale(self):
  a=covariance(40,[20],68,1,0,.5,.5)[0][0]; b=covariance(40,[20],68,1,0,.5,1)[0][0]
  self.assertAlmostEqual(4*a,b)
 def test_invalid(self):
  with self.assertRaises(ValueError): covariance(40,[20],68,1,1,1,1)
 def test_cutoff(self):
  with self.assertRaises(ValueError): weights(40,40)
if __name__=='__main__': unittest.main()
