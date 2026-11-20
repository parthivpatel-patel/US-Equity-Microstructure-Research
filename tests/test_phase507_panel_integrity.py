import unittest
from phase507_panel_integrity import audit_panel

R = {'AAA':'treated', 'BBB':'control'}
A = {'security':'AAA','date':'2025-10-02','exchange':'XNAS','group':'treated'}
B = {'security':'BBB','date':'2025-10-02','exchange':'XNAS','group':'control'}

class IntegrityTests(unittest.TestCase):
    def test_valid(self):
        v=audit_panel([A,B],R,allowed_dates=['2025-10-02'],allowed_exchanges=['XNAS'])
        self.assertEqual((v['rows'],v['treated_rows'],v['control_rows']), (2,1,1))
    def test_cross_exchange_allowed(self):
        v=audit_panel([A,dict(A,exchange='XNYS')],R)
        self.assertEqual(v['distinct_exchanges'],2)
    def test_duplicate_rejected(self):
        with self.assertRaisesRegex(ValueError,'duplicate'): audit_panel([A,dict(A)],R)
    def test_group_mismatch(self):
        with self.assertRaisesRegex(ValueError,'group mismatch'): audit_panel([dict(A,group='control')],R)
    def test_unknown_security(self):
        with self.assertRaisesRegex(ValueError,'unknown security'): audit_panel([dict(A,security='ZZZ')],R)
    def test_noncanonical_date(self):
        with self.assertRaises(ValueError): audit_panel([dict(A,date='20251002')],R)
    def test_invalid_calendar_day(self):
        with self.assertRaises(ValueError): audit_panel([dict(A,date='2025-09-31')],R)
    def test_date_allowlist(self):
        with self.assertRaisesRegex(ValueError,'date not allowed'): audit_panel([A],R,allowed_dates=['2025-10-03'])
    def test_exchange_allowlist(self):
        with self.assertRaisesRegex(ValueError,'exchange not allowed'): audit_panel([A],R,allowed_exchanges=['XNYS'])
    def test_empty(self):
        with self.assertRaisesRegex(ValueError,'empty panel'): audit_panel([],R)
    def test_boolean_roster(self):
        with self.assertRaisesRegex(ValueError,'invalid roster'): audit_panel([A],{'AAA':True})
    def test_missing_field(self):
        with self.assertRaisesRegex(ValueError,'missing field'): audit_panel([{'security':'AAA'}],R)

if __name__=='__main__': unittest.main()
