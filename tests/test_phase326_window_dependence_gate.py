"""Synthetic regression tests for Phase 326 (no SEC observations)."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from phase326_window_dependence_gate import audit

def row(wid,start,end,outcome='count'):
    return {'outcome':outcome,'window_id':wid,'start_date':start,'end_date':end,'placebo_pp':'0'}

class WindowGateTests(unittest.TestCase):
    def test_overlapping_boundary(self):
        r=audit([row('a','2025-09-01','2025-09-10'),row('b','2025-09-10','2025-09-20')])['count']
        self.assertEqual((r['overlapping_pairs'],r['largest_component_windows']),(1,2))
    def test_disjoint(self):
        r=audit([row('a','2025-09-01','2025-09-02'),row('b','2025-09-03','2025-09-04')])['count']
        self.assertEqual((r['overlapping_pairs'],r['overlap_connected_components']),(0,2))
    def test_transitive_component(self):
        r=audit([row('a','2025-09-01','2025-09-04'),row('b','2025-09-04','2025-09-08'),row('c','2025-09-08','2025-09-10')])['count']
        self.assertEqual((r['overlapping_pairs'],r['largest_component_windows']),(2,3))
    def test_duplicate(self):
        with self.assertRaises(ValueError): audit([row('a','2025-09-01','2025-09-02')]*2)
    def test_reform_date(self):
        with self.assertRaises(ValueError): audit([row('a','2025-11-01','2025-11-03')])
    def test_empty(self):
        with self.assertRaises(ValueError): audit([])
    def test_reversed(self):
        with self.assertRaises(ValueError): audit([row('a','2025-09-03','2025-09-01')])
    def test_separate_outcomes(self):
        r=audit([row('a','2025-09-01','2025-09-02'),row('a','2025-09-01','2025-09-02','volume')])
        self.assertEqual(set(r),{'count','volume'})

if __name__=='__main__': unittest.main()
