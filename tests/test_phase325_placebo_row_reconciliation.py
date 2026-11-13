"""Synthetic tests only; no SEC observations."""
import unittest
from scripts.phase325_placebo_row_reconciliation import reconcile
class TestPhase325(unittest.TestCase):
 def setUp(self):
  self.s=[dict(outcome='count',nov_minus_oct_pp='-1',pre_placebo_n='3',pre_placebo_at_least_as_negative='1',pre_placebo_at_least_as_extreme_absolute='2',pre_placebo_min_pp='-2',pre_placebo_max_pp='2')]
  self.r=[dict(outcome='count',window_id=str(i),start_date='2025-01-01',end_date='2025-01-02',placebo_pp=v) for i,v in enumerate(['-2','0','2'])]
 def test_match(self): self.assertTrue(reconcile(self.s,self.r)['count']['matches'])
 def test_mismatch(self):
  self.s[0]['pre_placebo_at_least_as_extreme_absolute']='1'
  self.assertFalse(reconcile(self.s,self.r)['count']['matches'])
 def test_duplicate(self):
  self.r[1]['window_id']='0'
  with self.assertRaises(ValueError): reconcile(self.s,self.r)
 def test_reversed_dates(self):
  self.r[0]['start_date']='2025-02-01'
  with self.assertRaises(ValueError): reconcile(self.s,self.r)
 def test_nonfinite(self):
  self.r[0]['placebo_pp']='NaN'
  with self.assertRaises(ValueError): reconcile(self.s,self.r)
 def test_unmatched_outcome(self):
  self.r[0]['outcome']='volume'
  with self.assertRaises(ValueError): reconcile(self.s,self.r)
 def test_ties(self):
  self.r[1]['placebo_pp']='-1'
  self.s[0].update(pre_placebo_at_least_as_negative='2',pre_placebo_at_least_as_extreme_absolute='3')
  x=reconcile(self.s,self.r)['count']
  self.assertEqual(x['ties_at_event'],1)
  self.assertTrue(x['matches'])
if __name__=='__main__': unittest.main()
