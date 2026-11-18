import unittest
from phase446_report_contract import audit

D='a'*64

def fixture():
    sub={'source_sha256':D,'source_bytes':100,'observations':2}
    a=dict(sub, **{'pass':True,'global_treatment_conflicts':[],
        'within_exchange_treatment_conflicts':[], 'within_exchange_group_changes':[],
        'permitted_cross_exchange_group_variation':['AAA']})
    return dict(sub, daily=dict(sub), calendar=dict(sub), assignment_scope=a,
                **{'pass':True,'treatment_authenticated':False,'historical_effect_estimated':False})

class ContractTests(unittest.TestCase):
    def test_valid(self): self.assertTrue(audit(fixture())['contract_valid'])
    def test_digest(self):
        r=fixture();r['calendar']['source_sha256']='b'*64
        with self.assertRaises(ValueError):audit(r)
    def test_count(self):
        r=fixture();r['assignment_scope']['observations']=1
        with self.assertRaises(ValueError):audit(r)
    def test_bool_as_count(self):
        r=fixture();r['source_bytes']=True
        with self.assertRaises(ValueError):audit(r)
    def test_false_pass_with_conflicts(self):
        r=fixture();r['assignment_scope']['global_treatment_conflicts']=['AAA'];r['assignment_scope']['pass']=False;r['pass']=False
        self.assertTrue(audit(r)['contract_valid'])
    def test_false_pass_without_conflicts(self):
        r=fixture();r['assignment_scope']['pass']=False;r['pass']=False
        with self.assertRaises(ValueError):audit(r)
    def test_true_pass_with_conflicts(self):
        r=fixture();r['assignment_scope']['global_treatment_conflicts']=['AAA']
        with self.assertRaises(ValueError):audit(r)
    def test_top_level_false_positive(self):
        r=fixture();r['assignment_scope']['global_treatment_conflicts']=['AAA'];r['assignment_scope']['pass']=False
        with self.assertRaises(ValueError):audit(r)
    def test_unverified_claim(self):
        r=fixture();r['treatment_authenticated']=True
        with self.assertRaises(ValueError):audit(r)
    def test_duplicate_conflicts(self):
        r=fixture();r['assignment_scope']['permitted_cross_exchange_group_variation']=['AAA','AAA']
        with self.assertRaises(ValueError):audit(r)

if __name__=='__main__':unittest.main()
