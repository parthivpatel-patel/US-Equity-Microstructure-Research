import importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/'scripts'/'phase432_daily_fixed_support.py'
spec=importlib.util.spec_from_file_location('phase432',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def row(d,s,a,e='X'):
    return dict(date=d,security=s,treated=str(a),exchange=e,match_group='G',hidden_count='1',total_count='2')
class Tests(unittest.TestCase):
    def test_fixed(self):
        x=[row(d,s,a) for d in ('2025-10-30','2025-10-31','2025-11-03') for s,a in [('T',1),('C',0)]]
        self.assertEqual(m.audit(x)['strict_support_units'],1)
    def test_churn(self):
        x=[row(d,s,a) for d,p in [('2025-10-30','1'),('2025-10-31','2'),('2025-11-03','3')] for s,a in [('T'+p,1),('C'+p,0)]]
        self.assertEqual(m.audit(x)['strict_support_units'],0)
    def test_missing_arm_on_day(self):
        x=[row(d,s,a) for d in ('2025-10-30','2025-11-03') for s,a in [('T',1),('C',0)]]+[row('2025-10-31','T',1)]
        self.assertEqual(m.audit(x)['strict_support_units'],0)
    def test_duplicate(self):
        with self.assertRaisesRegex(ValueError,'duplicate'):m.audit([row('2025-10-31','T',1)]*2)
    def test_unstable(self):
        self.assertEqual(m.audit([row('2025-10-31','T',1),row('2025-11-03','T',0)])['unstable_security_membership'],['T'])
    def test_empty(self):
        with self.assertRaisesRegex(ValueError,'empty'):m.audit([])
    def test_invalid(self):
        r=row('2025-10-31','T',1);r['hidden_count']='3'
        with self.assertRaisesRegex(ValueError,'bounds'):m.audit([r])
    def test_weekend(self):
        with self.assertRaisesRegex(ValueError,'day'):m.audit([row('2025-11-01','T',1)])
    def test_exchanges(self):
        x=[row(d,s,a,e) for e in ('X','Y') for d in ('2025-10-31','2025-11-03') for s,a in [('T',1),('C',0)]]
        self.assertEqual(m.audit(x)['strict_support_units'],2)
if __name__=='__main__':unittest.main()
