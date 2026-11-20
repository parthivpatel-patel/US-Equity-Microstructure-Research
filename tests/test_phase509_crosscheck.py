import unittest
from scripts.phase509_crosscheck import check_panel_coverage

P=[dict(security='A',date='2025-10-01',exchange='X',group='treated'),dict(security='B',date='2025-10-01',exchange='X',group='control')]
R={'A':'treated','B':'control'}
C=[dict(date='2025-10-01',exchange='X',period='pre',treated_eligible=1,treated_observed=1,control_eligible=1,control_observed=1)]
class Tests(unittest.TestCase):
    def test_match(self): self.assertTrue(check_panel_coverage(P,R,C)['consistent'])
    def test_mismatch(self): self.assertFalse(check_panel_coverage(P,R,[dict(C[0],control_observed=0)])['consistent'])
    def test_unexpected(self): self.assertFalse(check_panel_coverage(P,R,[dict(C[0],date='2025-10-02')])['consistent'])
    def test_duplicate_panel(self):
        with self.assertRaises(ValueError): check_panel_coverage(P+P[:1],R,C)
    def test_duplicate_coverage(self):
        with self.assertRaises(ValueError): check_panel_coverage(P,R,C+C)
    def test_bad_group(self):
        with self.assertRaises(ValueError): check_panel_coverage([dict(P[0],group='control')]+P[1:],R,C)
    def test_bad_date(self):
        with self.assertRaises(ValueError): check_panel_coverage([dict(P[0],date='2025-02-30')]+P[1:],R,C)
    def test_bad_period(self):
        with self.assertRaises(ValueError): check_panel_coverage(P,R,[dict(C[0],period='post')])
    def test_bool_counts(self):
        with self.assertRaises(ValueError): check_panel_coverage(P,R,[dict(C[0],treated_observed=True)])
    def test_empty_panel(self):
        with self.assertRaises(ValueError): check_panel_coverage([],R,C)
    def test_one_sided(self):
        self.assertFalse(check_panel_coverage(P,R,[dict(C[0],control_eligible=0,control_observed=0)])['consistent'])
if __name__=='__main__': unittest.main()
