import unittest
from datetime import date,timedelta
from phase203_hac_admission import audit_hac_input

def rows(n=24):
    d=date(2025,9,1); out=[]
    while len(out)<n:
        if d.weekday()<5:out.append({'date':d.isoformat(),'contrast':float(len(out))})
        d+=timedelta(days=1)
    return out

class TestAdmission(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(audit_hac_input(rows(),(0,1,3))['n_sessions'],24)
    def test_minimum(self):
        with self.assertRaises(ValueError):audit_hac_input(rows(19),(0,))
    def test_lag_too_large(self):
        with self.assertRaises(ValueError):audit_hac_input(rows(),(6,))
    def test_duplicate_lag(self):
        with self.assertRaises(ValueError):audit_hac_input(rows(),(1,1))
    def test_bool_lag(self):
        with self.assertRaises(ValueError):audit_hac_input(rows(),(True,))
    def test_duplicate_date(self):
        x=rows();x[1]=x[0]
        with self.assertRaises(ValueError):audit_hac_input(x,(0,))
    def test_weekend(self):
        x=rows();x[0]['date']='2025-09-06'
        with self.assertRaises(ValueError):audit_hac_input(x,(0,))
    def test_nonfinite(self):
        x=rows();x[0]['contrast']=float('nan')
        with self.assertRaises(ValueError):audit_hac_input(x,(0,))
    def test_not_authenticated(self):
        self.assertFalse(audit_hac_input(rows(),(0,))['source_authenticated'])
    def test_invalid_fraction(self):
        with self.assertRaises(ValueError):audit_hac_input(rows(),(0,),max_lag_fraction=1)

if __name__=='__main__':unittest.main()
