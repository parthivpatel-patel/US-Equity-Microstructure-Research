import unittest
from scripts.phase307_eligibility import audit
S=['2025-10-30','2025-10-31','2025-11-03']
I=[('ABC','XNAS',S[1],S[2])]
class TestEligibility(unittest.TestCase):
    def test_complete(self):
        r=audit([('ABC','XNAS',d) for d in S[1:]],I,S)
        self.assertEqual((r['missing'],r['unexpected'],r['expected_cells']),([],[],2))
    def test_missing(self): self.assertEqual(len(audit([],I,S)['missing']),2)
    def test_unexpected(self): self.assertEqual(len(audit([('ABC','XNAS',S[0])],I,S)['unexpected']),1)
    def test_duplicate(self): self.assertEqual(len(audit([('ABC','XNAS',S[1])]*2,I,S)['duplicates']),1)
    def test_overlap(self):
        with self.assertRaises(ValueError): audit([],I+[('ABC','XNAS',S[0],S[1])],S)
    def test_adjacent(self):
        self.assertEqual(audit([], [('ABC','XNAS',S[0],S[0]),('ABC','XNAS',S[1],S[2])],S)['expected_cells'],3)
    def test_reversed(self):
        with self.assertRaises(ValueError): audit([], [('A','X',S[2],S[0])],S)
    def test_unsorted(self):
        with self.assertRaises(ValueError): audit([],I,S[::-1])
    def test_weekend(self):
        with self.assertRaises(ValueError): audit([],I,['2025-11-01'])
    def test_empty_interval(self):
        self.assertEqual(len(audit([], [('A','X','2025-10-01','2025-10-02')],S)['empty_intervals']),1)
    def test_flags(self):
        r=audit([],I,S)
        self.assertFalse(any(r[k] for k in ('source_authenticated','eligibility_authenticated','calendar_authenticated','causal_inference_authorized')))
    def test_noncanonical(self):
        with self.assertRaises(ValueError): audit([],I,['2025-1-2'])
if __name__=='__main__': unittest.main()
