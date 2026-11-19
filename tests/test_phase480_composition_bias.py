import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from phase480_composition_bias import audit,example

class TestComposition(unittest.TestCase):
    def test_balanced_zero(self):
        a,_=example(); self.assertEqual(a['observed_contrast'],0)
    def test_missing_creates_spurious_one(self):
        _,b=example(); self.assertEqual(b['observed_contrast'],1)
    def test_complete_case_zero(self):
        _,b=example(); self.assertEqual(b['complete_case_contrast'],0)
        self.assertEqual(b['complete_pairs'],1)
    def test_equal_levels_immune(self):
        self.assertEqual(audit([2,2],[[True]*4,[True,True,False,False]])['observed_contrast'],0)
    def test_no_complete_cases(self):
        r=audit([1,-1],[[True,True,False,False],[False,False,True,True]])
        self.assertIsNone(r['complete_case_contrast'])
    def test_empty_date_rejected(self):
        with self.assertRaises(ValueError): audit([1],[[True,False,True,True]])
    def test_weights_change_magnitude(self):
        r=audit([1,-1],[[True]*4,[True,True,False,False]],[1,3]); self.assertEqual(r['observed_contrast'],1.5)
    def test_invalid_cutoff(self):
        with self.assertRaises(ValueError): audit([1],[[True]*4],cutoff=4)

if __name__=='__main__': unittest.main()
