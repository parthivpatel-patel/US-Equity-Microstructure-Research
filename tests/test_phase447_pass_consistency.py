import copy
import unittest
from phase447_pass_consistency import audit


def fixture():
    base={'source_sha256':'a'*64,'source_bytes':20,'observations':2,'pass':True}
    assignment=dict(base,global_treatment_conflicts=[],within_exchange_treatment_conflicts=[],within_exchange_group_changes=[],permitted_cross_exchange_group_variation=[])
    return dict(base,daily=copy.deepcopy(base),calendar=copy.deepcopy(base),assignment_scope=assignment,treatment_authenticated=False,historical_effect_estimated=False)


class Tests(unittest.TestCase):
    def test_valid(self): self.assertTrue(audit(fixture())['panel_pass'])
    def test_daily_failure_cannot_be_masked(self):
        r=fixture();r['daily']['pass']=False
        with self.assertRaisesRegex(ValueError,'top-level'):audit(r)
    def test_calendar_failure_cannot_be_masked(self):
        r=fixture();r['calendar']['pass']=False
        with self.assertRaisesRegex(ValueError,'top-level'):audit(r)
    def test_daily_failure_propagated(self):
        r=fixture();r['daily']['pass']=False;r['pass']=False
        self.assertFalse(audit(r)['panel_pass'])
    def test_calendar_failure_propagated(self):
        r=fixture();r['calendar']['pass']=False;r['pass']=False
        self.assertFalse(audit(r)['panel_pass'])
    def test_assignment_failure_propagated(self):
        r=fixture();r['assignment_scope']['global_treatment_conflicts']=['AAA'];r['assignment_scope']['pass']=False;r['pass']=False
        self.assertFalse(audit(r)['panel_pass'])
    def test_missing_daily_flag(self):
        r=fixture();del r['daily']['pass']
        with self.assertRaisesRegex(ValueError,'daily'):audit(r)
    def test_integer_calendar_flag(self):
        r=fixture();r['calendar']['pass']=1
        with self.assertRaisesRegex(ValueError,'calendar'):audit(r)
    def test_top_level_false_when_all_pass(self):
        r=fixture();r['pass']=False
        with self.assertRaisesRegex(ValueError,'top-level'):audit(r)
    def test_source_mismatch_still_rejected(self):
        r=fixture();r['daily']['source_sha256']='b'*64
        with self.assertRaisesRegex(ValueError,'source mismatch'):audit(r)


if __name__=='__main__': unittest.main()
