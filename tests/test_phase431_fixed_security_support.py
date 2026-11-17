import importlib.util
from pathlib import Path
import unittest
path=Path(__file__).resolve().parents[1]/'scripts'/'phase431_fixed_security_support.py'
spec=importlib.util.spec_from_file_location('phase431',path)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def row(date,security,treated,group='g',exchange='X',hidden='1',total='2'):
    return dict(date=date,security=security,treated=str(treated),match_group=group,exchange=exchange,hidden_count=hidden,total_count=total)
class AuditTests(unittest.TestCase):
    def test_fixed_pair(self):
        x=[row(d,s,a) for d in ('2025-10-31','2025-11-03') for s,a in [('T',1),('C',0)]]
        self.assertEqual(m.audit(x)['fixed_security_paired_units'],1)
    def test_churn_not_fixed(self):
        x=[row('2025-10-31','T1',1),row('2025-10-31','C1',0),row('2025-11-03','T2',1),row('2025-11-03','C2',0)]
        r=m.audit(x)
        self.assertEqual(r['pre_post_paired_units'],1)
        self.assertEqual(r['fixed_security_paired_units'],0)
        self.assertFalse(r['estimation_ready'])
    def test_duplicate(self):
        with self.assertRaisesRegex(ValueError,'duplicate'): m.audit([row('2025-11-03','A',1)]*2)
    def test_membership_shift(self):
        r=m.audit([row('2025-10-31','A',1),row('2025-11-03','A',0)])
        self.assertEqual(r['unstable_security_membership'],['A'])
    def test_invalid_count(self):
        with self.assertRaisesRegex(ValueError,'count bounds'): m.audit([row('2025-11-03','A',1,hidden='3')])
    def test_weekend(self):
        with self.assertRaisesRegex(ValueError,'weekend'): m.audit([row('2025-11-01','A',1)])
    def test_empty(self):
        with self.assertRaisesRegex(ValueError,'empty'): m.audit([])
    def test_missing_field(self):
        with self.assertRaisesRegex(ValueError,'missing'): m.audit([{'date':'2025-11-03'}])
    def test_multiple_exchanges(self):
        x=[row(d,s,a,exchange=e) for e in ('X','Y') for d in ('2025-10-31','2025-11-03') for s,a in [('T',1),('C',0)]]
        self.assertEqual(m.audit(x)['fixed_security_paired_units'],2)
if __name__=='__main__': unittest.main()
