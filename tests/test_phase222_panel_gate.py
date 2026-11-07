import unittest
from scripts.phase222_panel_gate import audit_panel

def fixture():
    dates=['2025-10-01','2025-10-02']
    rows=[{'date':d,'security':s,'exchange':e,'hidden_count':1,'total_count':4}
          for d in dates for s in ['T','C'] for e in ['X','Y']]
    return rows,dates,['T'],['C'],['X','Y']

class PanelGateTests(unittest.TestCase):
    def test_complete(self):
        out=audit_panel(*fixture())
        self.assertEqual(out['cells'],8)
        self.assertFalse(out['source_authenticated'])
    def test_missing_cell(self):
        a=list(fixture()); a[0]=a[0][:-1]
        with self.assertRaisesRegex(ValueError,'incomplete'): audit_panel(*a)
    def test_duplicate_cell(self):
        a=list(fixture()); a[0]=a[0]+[dict(a[0][0])]
        with self.assertRaisesRegex(ValueError,'duplicate'): audit_panel(*a)
    def test_overlap(self):
        a=list(fixture()); a[3]=['T']
        with self.assertRaises(ValueError): audit_panel(*a)
    def test_unknown_exchange(self):
        a=list(fixture()); a[0][0]['exchange']='Z'
        with self.assertRaises(ValueError): audit_panel(*a)
    def test_invalid_denominator(self):
        a=list(fixture()); a[0][0]['total_count']=0
        with self.assertRaises(ValueError): audit_panel(*a)
    def test_hidden_exceeds_total(self):
        a=list(fixture()); a[0][0]['hidden_count']=5
        with self.assertRaises(ValueError): audit_panel(*a)
    def test_reform_intrusion(self):
        a=list(fixture()); a[1][-1]='2025-11-03'
        with self.assertRaises(ValueError): audit_panel(*a)
    def test_ambiguous_float_count(self):
        a=list(fixture()); a[0][0]['hidden_count']=1.0
        with self.assertRaises(ValueError): audit_panel(*a)

if __name__=='__main__': unittest.main()
