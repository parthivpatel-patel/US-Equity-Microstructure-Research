import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from phase207_fixed_roster import audit_fixed_roster

D = ['2025-10-01','2025-10-02']
def panel():
    return [dict(date=d,security=s,exchange='XNAS',group='m1',treatment=t,outcome=o,value=1.0)
            for d in D for s,t in [('AAA',1),('BBB',0)] for o in ('count','volume')]

class AuditTests(unittest.TestCase):
    def test_valid(self): self.assertTrue(audit_fixed_roster(panel(),D)['admitted'])
    def test_missing(self): self.assertIn('missing_cells',audit_fixed_roster(panel()[:-1],D)['errors'])
    def test_duplicate(self): self.assertIn('duplicate_cell',audit_fixed_roster(panel()+panel()[:1],D)['errors'])
    def test_switch(self):
        r=panel();r[0]['treatment']=0
        self.assertIn('identity_switch',audit_fixed_roster(r,D)['errors'])
    def test_unmatched(self):
        r=[x for x in panel() if x['security']=='AAA']
        self.assertIn('unmatched_group',audit_fixed_roster(r,D)['errors'])
    def test_unexpected_date(self):
        r=panel();r[0]['date']='2025-10-03'
        self.assertIn('unexpected_date',audit_fixed_roster(r,D)['errors'])
    def test_unexpected_outcome(self):
        r=panel();r[0]['outcome']='price'
        self.assertIn('unexpected_outcome',audit_fixed_roster(r,D)['errors'])
    def test_nonfinite(self):
        r=panel();r[0]['value']=float('nan')
        self.assertIn('invalid_value',audit_fixed_roster(r,D)['errors'])
    def test_empty(self): self.assertIn('empty_panel',audit_fixed_roster([],D)['errors'])
    def test_duplicate_calendar(self): self.assertIn('duplicate_calendar',audit_fixed_roster(panel(),D+D)['errors'])
    def test_exchange_distinction(self):
        r=panel();r[0]['exchange']='XNYS'
        self.assertIn('missing_cells',audit_fixed_roster(r,D)['errors'])
    def test_malformed(self): self.assertIn('malformed_row',audit_fixed_roster([{}],D)['errors'])

if __name__=='__main__': unittest.main()
