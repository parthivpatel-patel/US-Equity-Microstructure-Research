"""Deterministic constructed-data checks; not SEC observations."""
import unittest
from scripts.phase456_support_sensitivity import compare

def row(s,e,g,d,t,y):
    return dict(security=s,exchange=e,matched_group=g,date=d,treated=t,outcome=y)

class SupportSensitivityTests(unittest.TestCase):
    def test_identical_support(self):
        r=[]
        for d,a in [("2025-10-30",2),("2025-11-04",5)]:
            r += [row("T","X","G",d,True,a),row("C","X","G",d,False,0)]
        z=compare(r)
        self.assertEqual(z["local"]["estimate"],3)
        self.assertEqual(z["globally_balanced"]["estimate"],3)
        self.assertEqual(z["difference_global_minus_local"],0)
    def test_selection_changes_estimate(self):
        r=[]
        for g in ("A","B"):
            for d,v in [("2025-10-30",0),("2025-11-04",2)]:
                r += [row("T"+g,"X",g,d,True,v),row("C"+g,"X",g,d,False,0)]
        r += [row("TA","X","A","2025-11-05",True,20),row("CA","X","A","2025-11-05",False,0)]
        z=compare(r)
        self.assertAlmostEqual(z["local"]["estimate"],6.5)
        self.assertAlmostEqual(z["globally_balanced"]["estimate"],2)
        self.assertAlmostEqual(z["difference_global_minus_local"],-4.5)
    def test_missing_pre_returns_none(self):
        r=[row("T","X","G","2025-11-04",True,1),row("C","X","G","2025-11-04",False,0)]
        self.assertIsNone(compare(r)["local"]["estimate"])
    def test_duplicate_rejected(self):
        r=[row("T","X","G","2025-11-04",True,1)]*2
        with self.assertRaises(ValueError): compare(r)
    def test_unstable_assignment_rejected(self):
        r=[row("T","X","G","2025-10-30",True,1),row("T","X","H","2025-11-04",True,2)]
        with self.assertRaises(ValueError): compare(r)
    def test_nonfinite_rejected(self):
        with self.assertRaises(ValueError): compare([row("T","X","G","2025-11-04",True,float("nan"))])

if __name__=="__main__":
    unittest.main()
