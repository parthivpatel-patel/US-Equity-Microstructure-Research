import unittest
from phase445_scope_adjudication import adjudicate
H='a'*64

def reports():
    d=dict(source_sha256=H,source_bytes=100,observations=4,unstable_security_membership=['ABC'],strict_support_units=2,group_exchange_units=2)
    a=dict(source_sha256=H,source_bytes=100,observations=4,permitted_cross_exchange_group_variation=['ABC'],global_treatment_conflicts=[],within_exchange_group_changes=[],within_exchange_treatment_conflicts=[],**{'pass':True})
    return d,a

class Tests(unittest.TestCase):
    def test_permitted_cross_exchange(self):
        d,a=reports(); r=adjudicate(d,a); self.assertTrue(r['pass']); self.assertEqual(r['explained_cross_exchange_flags'],['ABC'])
    def test_unexplained_flag(self):
        d,a=reports();a['permitted_cross_exchange_group_variation']=[];self.assertFalse(adjudicate(d,a)['pass'])
    def test_treatment_conflict(self):
        d,a=reports();a['global_treatment_conflicts']=['ABC'];self.assertFalse(adjudicate(d,a)['pass'])
    def test_local_conflict(self):
        d,a=reports();a['within_exchange_group_changes']=['ABC@X'];self.assertFalse(adjudicate(d,a)['pass'])
    def test_incomplete_support(self):
        d,a=reports();d['strict_support_units']=1;self.assertFalse(adjudicate(d,a)['pass'])
    def test_digest_mismatch(self):
        d,a=reports();a['source_sha256']='b'*64
        with self.assertRaises(ValueError):adjudicate(d,a)
    def test_missing_conflicts(self):
        d,a=reports();del a['within_exchange_group_changes']
        with self.assertRaises(ValueError):adjudicate(d,a)
    def test_inconsistent_count(self):
        d,a=reports();a['observations']=5
        with self.assertRaises(ValueError):adjudicate(d,a)
    def test_assignment_fail(self):
        d,a=reports();a['pass']=False;self.assertFalse(adjudicate(d,a)['pass'])

if __name__=='__main__':unittest.main()
