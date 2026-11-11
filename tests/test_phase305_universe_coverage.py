import unittest
from phase305_universe_coverage import audit_declared_universe as audit

class UniverseCoverageTests(unittest.TestCase):
    def test_entirely_absent_pair(self):
        out = audit([{"security":"A","exchange":"X","date":"2025-09-02"}], [("A","X"),("B","Y")], ["2025-09-02"])
        self.assertEqual(out["entirely_absent_pairs"], [("B","Y")])
        self.assertEqual(out["missing_cells"], [("B","Y","2025-09-02")])
    def test_complete(self):
        out = audit([{"security":"A","exchange":"X","date":"2025-09-02"}], [("A","X")], ["2025-09-02"])
        self.assertTrue(out["structurally_complete"])
        self.assertFalse(out["source_authenticated"])
    def test_duplicate(self):
        row = {"security":"A","exchange":"X","date":"2025-09-02"}
        self.assertEqual(audit([row,row], [("A","X")], ["2025-09-02"])["duplicate_cells"], [("A","X","2025-09-02",2)])
    def test_unexpected(self):
        row = {"security":"B","exchange":"Y","date":"2025-09-02"}
        self.assertEqual(len(audit([row], [("A","X")], ["2025-09-02"])["unexpected_cells"]), 1)
    def test_duplicate_declared_pairs(self):
        with self.assertRaises(ValueError): audit([], [("A","X"),("A","X")], ["2025-09-02"])
    def test_weekend(self):
        with self.assertRaises(ValueError): audit([], [("A","X")], ["2025-09-06"])
    def test_noncanonical(self):
        with self.assertRaises(ValueError): audit([], [("A","X")], ["2025-9-2"])
    def test_empty_rows(self):
        self.assertEqual(audit([], [("A","X")], ["2025-09-02"])["entirely_absent_pairs"], [("A","X")])
    def test_undeclared_date(self):
        row = {"security":"A","exchange":"X","date":"2025-09-03"}
        self.assertEqual(len(audit([row], [("A","X")], ["2025-09-02"])["unexpected_cells"]), 1)
if __name__ == "__main__": unittest.main()
