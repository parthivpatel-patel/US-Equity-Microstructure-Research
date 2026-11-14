import unittest
from phase357_coverage_audit import audit_coverage

S=['2025-10-01','2025-10-02']; T=['AAA']; E=['X','Y']
def rows(): return [('AAA',d,e,'observed',0 if d==S[0] else 5) for d in S for e in E]
class CoverageTests(unittest.TestCase):
    def test_balanced(self):
        r=audit_coverage(rows(),S,T,E)
        self.assertEqual((r['cells'],r['observed_zero_cells'],r['fully_observed_security_dates']),(4,2,2))
    def test_missing_distinct_from_zero(self):
        a=rows(); a[0]=('AAA',S[0],'X','source_missing',None)
        r=audit_coverage(a,S,T,E)
        self.assertEqual((r['status_counts']['source_missing'],r['observed_zero_cells'],r['fully_observed_security_dates']),(1,1,1))
    def test_duplicate_rejected(self):
        with self.assertRaisesRegex(ValueError,'duplicate'): audit_coverage(rows()+[rows()[0]],S,T,E)
    def test_undeclared_rejected(self):
        with self.assertRaisesRegex(ValueError,'undeclared'): audit_coverage(rows()[:-1],S,T,E)
    def test_nonobserved_value_rejected(self):
        a=rows(); a[0]=('AAA',S[0],'X','not_listed',0)
        with self.assertRaisesRegex(ValueError,'non-observed'): audit_coverage(a,S,T,E)
    def test_nonfinite_rejected(self):
        a=rows(); a[0]=('AAA',S[0],'X','observed',float('nan'))
        with self.assertRaisesRegex(ValueError,'invalid observed'): audit_coverage(a,S,T,E)
    def test_negative_rejected(self):
        a=rows(); a[0]=('AAA',S[0],'X','observed',-1)
        with self.assertRaises(ValueError): audit_coverage(a,S,T,E)
    def test_off_universe_rejected(self):
        a=rows(); a[0]=('AAA',S[0],'Z','observed',0)
        with self.assertRaisesRegex(ValueError,'out-of-universe'): audit_coverage(a,S,T,E)
    def test_noncanonical_date_rejected(self):
        with self.assertRaises(ValueError): audit_coverage([],['2025-1-1'],T,E)
    def test_unordered_dates_rejected(self):
        with self.assertRaises(ValueError): audit_coverage([],S[::-1],T,E)
if __name__=='__main__': unittest.main()
