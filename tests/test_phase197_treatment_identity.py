import unittest
from scripts.phase197_treatment_identity import audit

def rec(w,d,t,o='count',g='G',s='ABC',e='X'):
    return dict(window=w,date=d,treated=t,outcome=o,group=g,security=s,exchange=e)

class AuditTests(unittest.TestCase):
    def test_stable_disjoint(self):
        rows=[rec(w,d,True,o) for w,d in [('pre','2025-10-06'),('post','2025-11-03')] for o in ('count','volume')]
        r=audit(rows)
        self.assertEqual(r['treatment_switches'],[])
        self.assertEqual(r['unpaired_keys'],[])
        self.assertFalse(r['treatment_authenticated'])
    def test_switch(self):
        self.assertEqual(audit([rec('a','2025-10-06',False),rec('b','2025-11-03',True)])['treatment_switches'],[['ABC','X']])
    def test_group_switch(self):
        self.assertEqual(audit([rec('a','2025-10-06',True),rec('b','2025-11-03',True,g='H')])['group_switches'],[['ABC','X']])
    def test_missing_pair(self):
        self.assertEqual(len(audit([rec('a','2025-10-06',True)])['unpaired_keys']),1)
    def test_duplicate(self):
        with self.assertRaises(ValueError): audit([rec('a','2025-10-06',True)]*2)
    def test_weekend(self):
        with self.assertRaises(ValueError): audit([rec('a','2025-10-05',True)])
    def test_non_boolean(self):
        with self.assertRaises(ValueError): audit([rec('a','2025-10-06',1)])
    def test_invalid_outcome(self):
        with self.assertRaises(ValueError): audit([rec('a','2025-10-06',True,'other')])
    def test_distinct_exchanges(self):
        r=audit([rec('a','2025-10-06',False,e='X'),rec('b','2025-11-03',True,e='Y')])
        self.assertEqual(r['treatment_switches'],[])
    def test_missing_field(self):
        row=rec('a','2025-10-06',True); del row['security']
        with self.assertRaises(ValueError): audit([row])
if __name__=='__main__': unittest.main()
