import unittest
from fractions import Fraction
from scripts.phase388_hac_bandwidth_audit import audit_bandwidths

DATES = ["2025-09-02","2025-09-03","2025-09-04","2025-09-05"]
def panel(values):
    return [(p,d,v) for p in ("A","B") for d,v in zip(DATES,values)]

class AuditTests(unittest.TestCase):
    def test_exact_known_example(self):
        a=audit_bandwidths(panel([0,1,0,1]),[0,1])
        self.assertEqual(a["mean"],Fraction(1,2))
        self.assertEqual(a["results"][0]["variance_of_mean"],Fraction(1,16))
        self.assertEqual(a["results"][1]["variance_of_mean"],Fraction(1,64))
    def test_common_date_shock_preserved(self):
        self.assertEqual(audit_bandwidths(panel([0,1,0,1]),[0])["n_pairs"],2)
    def test_zero_warning(self):
        self.assertTrue(all(x["zero_variance_warning"] for x in audit_bandwidths(panel([1,1,1,1]),[0,1])["results"]))
    def test_order_invariant(self):
        x=panel([0,1,0,1])
        self.assertEqual(audit_bandwidths(x,[0,1]),audit_bandwidths(x[::-1],[0,1]))
    def test_duplicate_rejected(self):
        x=panel([0,1,0,1])
        self.assertRaises(ValueError,audit_bandwidths,x+[x[0]],[0])
    def test_missing_rejected(self):
        self.assertRaises(ValueError,audit_bandwidths,panel([0,1,0,1])[:-1],[0])
    def test_bad_bandwidth(self):
        self.assertRaises(ValueError,audit_bandwidths,panel([0,1,0,1]),[4])
    def test_duplicate_bandwidth(self):
        self.assertRaises(ValueError,audit_bandwidths,panel([0,1,0,1]),[1,1])
    def test_boolean_gap_rejected(self):
        x=panel([0,1,0,1]);x[0]=("A",DATES[0],True)
        self.assertRaises(ValueError,audit_bandwidths,x,[0])
    def test_invalid_date(self):
        x=panel([0,1,0,1]);x[0]=("A","2025-09-99",0)
        self.assertRaises(ValueError,audit_bandwidths,x,[0])
if __name__=="__main__":
    unittest.main()
