"""Deterministic regression tests for Phase 441; no historical observations."""
import unittest
from scripts.phase441_assignment_scope import audit

def row(s='A',e='X',g='G',a='1'):
    return dict(security=s,exchange=e,match_group=g,treated=a)

class TestAssignmentScope(unittest.TestCase):
    def test_simple(self): self.assertTrue(audit([row()])['structurally_eligible'])
    def test_cross_exchange_groups(self):
        r=audit([row(e='X',g='G1'),row(e='Y',g='G2')])
        self.assertTrue(r['structurally_eligible'])
        self.assertEqual(r['cross_exchange_only_group_variation'],['A'])
    def test_global_treatment_conflict(self):
        r=audit([row(e='X',a='0'),row(e='Y',a='1')])
        self.assertFalse(r['structurally_eligible'])
        self.assertEqual(r['global_treatment_conflicts'],['A'])
        self.assertEqual(r['within_exchange_treatment_conflicts'],[])
    def test_local_group_conflict(self):
        self.assertFalse(audit([row(g='G1'),row(g='G2')])['structurally_eligible'])
    def test_local_arm_conflict(self):
        self.assertEqual(audit([row(a='0'),row(a='1')])['within_exchange_treatment_conflicts'],['A@X'])
    def test_empty(self):
        with self.assertRaises(ValueError): audit([])
    def test_missing(self):
        with self.assertRaises(ValueError): audit([{'security':'A'}])
    def test_bad_arm(self):
        with self.assertRaises(ValueError): audit([row(a='2')])
    def test_blank(self):
        with self.assertRaises(ValueError): audit([row(s=' ')])
    def test_not_authenticated(self):
        self.assertFalse(audit([row()])['treatment_authenticated'])
if __name__=='__main__': unittest.main()
