import unittest
from phase462_joint_placebo_bootstrap import joint_placebo_bootstrap as run

D=['2025-09-01','2025-09-02','2025-09-03','2025-09-04','2025-09-05','2025-09-08']
G={('X','A'):dict(zip(D,[0,0,1,1,2,2])),('Y','B'):dict(zip(D,[0,0,2,2,4,4]))}
C=['2025-09-03','2025-09-05']
class TestJoint(unittest.TestCase):
 def test_exact_observed(self):
  a=run(G,D,C,repetitions=100,seed=4)
  self.assertAlmostEqual(a['placebos'][0]['observed'],2.25)
  self.assertAlmostEqual(a['placebos'][1]['observed'],2.25)
 def test_deterministic(self):
  self.assertEqual(run(G,D,C,repetitions=100,seed=5),run(G,D,C,repetitions=100,seed=5))
 def test_reject_incomplete(self):
  g={('X','A'):{D[0]:1}}
  with self.assertRaises(ValueError):run(g,D,C)
 def test_reject_duplicate_sessions(self):
  with self.assertRaises(ValueError):run(G,D+[D[-1]],C)
 def test_reject_invalid_gap(self):
  g={('X','A'):dict(zip(D,[0,0,1,1,2,float('nan')]))}
  with self.assertRaises(ValueError):run(g,D,C)
 def test_reject_outside_cutoff(self):
  with self.assertRaises(ValueError):run(G,D,['2025-08-01'])
 def test_reject_invalid_block(self):
  with self.assertRaises(ValueError):run(G,D,C,block_length=7)
 def test_joint_draw_count(self):
  a=run(G,D,C,repetitions=200,seed=2)
  self.assertEqual(len(a['placebos']),2)
  self.assertLessEqual(a['complete_draws'],200)
  self.assertGreater(a['complete_draws'],0)
if __name__=='__main__': unittest.main()
