import unittest
from phase394_placebo_overlap import audit

class TestOverlap(unittest.TestCase):
    def test_disjoint(self):
        x=audit([{"id":"a","sessions":["2025-10-01"]},{"id":"b","sessions":["2025-10-02"]}])
        self.assertEqual(x["overlapping_pairs"],0)
        self.assertEqual(x["session_reuse_effective_count"],2)
    def test_identical(self):
        x=audit([{"id":"a","sessions":["2025-10-01"]},{"id":"b","sessions":["2025-10-01"]}])
        self.assertEqual(x["identical_window_pairs"],1)
        self.assertEqual(x["session_reuse_effective_count"],1)
    def test_partial(self):
        x=audit([{"id":"a","sessions":["2025-10-01","2025-10-02"]},{"id":"b","sessions":["2025-10-02","2025-10-03"]}])
        self.assertEqual(x["pairs"][0]["jaccard"],1/3)
        self.assertEqual(x["session_reuse_effective_count"],16/6)
    def test_order_invariance(self):
        r=[{"id":"z","sessions":["2025-10-02"]},{"id":"a","sessions":["2025-10-01","2025-10-02"]}]
        self.assertEqual(audit(r),audit(list(reversed(r))))
    def test_duplicate_id(self):
        with self.assertRaises(ValueError): audit([{"id":"a","sessions":["2025-10-01"]}]*2)
    def test_duplicate_session(self):
        with self.assertRaises(ValueError): audit([{"id":"a","sessions":["2025-10-01"]*2}])
    def test_bad_date(self):
        with self.assertRaises(ValueError): audit([{"id":"a","sessions":["2025-02-30"]}])
    def test_empty(self):
        with self.assertRaises(ValueError): audit([])
    def test_missing(self):
        with self.assertRaises(ValueError): audit([{"id":"a"}])

if __name__=="__main__": unittest.main()
