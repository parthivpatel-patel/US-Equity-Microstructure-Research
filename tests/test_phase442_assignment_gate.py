"""Deterministic tests for Phase 442 assignment scope."""
import unittest
from scripts.phase442_assignment_gate import evaluate

def r(day='2025-10-01', security='AAA', exchange='X', group='G1', arm='1'):
    return dict(date=day,security=security,exchange=exchange,match_group=group,treated=arm)

class AssignmentGateTests(unittest.TestCase):
    def test_cross_exchange_group_permitted(self):
        x=evaluate([r(),r(exchange='Y',group='G2')])
        self.assertTrue(x['pass'])
        self.assertEqual(x['permitted_cross_exchange_group_variation'],['AAA'])
    def test_global_conflict(self):
        x=evaluate([r(),r(exchange='Y',arm='0')])
        self.assertFalse(x['pass'])
        self.assertEqual(x['global_treatment_conflicts'],['AAA'])
    def test_local_group_change(self):
        x=evaluate([r(),r(day='2025-10-02',group='G2')])
        self.assertEqual(x['within_exchange_group_changes'],['AAA@X'])
        self.assertFalse(x['pass'])
    def test_local_arm_change(self):
        self.assertFalse(evaluate([r(),r(day='2025-10-02',arm='0')])['pass'])
    def test_duplicate(self):
        with self.assertRaisesRegex(ValueError,'duplicate'): evaluate([r(),r()])
    def test_empty(self):
        with self.assertRaisesRegex(ValueError,'empty'): evaluate([])
    def test_weekend(self):
        with self.assertRaisesRegex(ValueError,'date'): evaluate([r(day='2025-11-01')])
    def test_invalid_arm(self):
        with self.assertRaisesRegex(ValueError,'treatment'): evaluate([r(arm='2')])
    def test_two_securities(self):
        self.assertTrue(evaluate([r(),r(security='BBB',arm='0')])['pass'])
    def test_not_authenticated(self):
        self.assertFalse(evaluate([r()])['treatment_authenticated'])

if __name__=='__main__': unittest.main()
