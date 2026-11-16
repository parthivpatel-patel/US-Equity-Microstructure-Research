import unittest
from scripts.phase407_identification_gate import audit
def row(d='2025-09-02',t='1',g='A',security='T'):
 return dict(date=d,security=security,exchange='XNAS',treated=t,match_group=g,hidden_trades='1',total_trades='2',hidden_shares='3',total_shares='4')
class TestGate(unittest.TestCase):
 def test_valid_structure_not_authenticated(self):
  a=audit([row(),row(t='0',security='C'),row(d='2025-10-02'),row(d='2025-11-03')]);self.assertEqual(a['status'],'STRUCTURALLY_ELIGIBLE_NOT_AUTHENTICATED')
 def test_missing_september(self):
  a=audit([row(d='2025-10-02'),row(d='2025-10-02',t='0',security='C'),row(d='2025-11-03')]);self.assertIn('no September 2025 pretrend dates',a['errors'])
 def test_duplicate(self):
  a=audit([row(),row(),row(t='0',security='C')]);self.assertTrue(any('duplicate' in e for e in a['errors']))
 def test_bad_denominator(self):
  r=row();r['total_trades']='0';self.assertTrue(any('numerator/denominator' in e for e in audit([r])['errors']))
 def test_no_matching(self):
  self.assertTrue(any('matched groups' in e for e in audit([row()])['errors']))
if __name__=='__main__':unittest.main()
