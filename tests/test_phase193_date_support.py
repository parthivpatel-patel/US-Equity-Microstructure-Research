import unittest
from scripts.phase193_date_support import audit

def row(w,d,g,o):
    return dict(window_id=w,trade_date=d,matched_group_id=g,outcome=o)

class DateSupportTests(unittest.TestCase):
    def test_identical_counts_not_identical_dates(self):
        rows=[]
        for w,d in [('pre','2025-10-01'),('post','2025-10-02')]:
            for o in ('count','volume'): rows.append(row(w,d,'G1',o))
        result=audit(rows)
        self.assertEqual(result['all_window_common_unit_dates'],0)
        self.assertEqual(result['paired_unit_dates_per_window'],{'post':1,'pre':1})
    def test_common_unit_date(self):
        rows=[row(w,'2025-10-01','G1',o) for w in ('a','b') for o in ('count','volume')]
        self.assertEqual(audit(rows)['all_window_common_unit_dates'],1)
    def test_different_groups_no_overlap(self):
        rows=[row(w,'2025-10-01',g,o) for w,g in [('a','G1'),('b','G2')] for o in ('count','volume')]
        self.assertEqual(audit(rows)['all_window_common_unit_dates'],0)
    def test_duplicate(self):
        rows=[row('a','2025-10-01','G1','count')]*2
        with self.assertRaisesRegex(ValueError,'duplicate'): audit(rows)
    def test_weekend(self):
        with self.assertRaisesRegex(ValueError,'date'): audit([row('a','2025-10-04','G1','count')])
    def test_missing_outcome(self):
        with self.assertRaisesRegex(ValueError,'both outcomes'): audit([row('a','2025-10-01','G1','count')])
    def test_noncanonical_date(self):
        with self.assertRaisesRegex(ValueError,'date'): audit([row('a','2025-1-1','G1','count')])
    def test_empty(self):
        with self.assertRaisesRegex(ValueError,'empty'): audit([])

if __name__=='__main__': unittest.main()
