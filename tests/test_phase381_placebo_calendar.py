import sys
import unittest
from datetime import date
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from phase381_placebo_calendar import audit_placebo_calendar as audit

D = lambda s: date.fromisoformat(s)
S = [D(s) for s in ['2025-10-29','2025-10-30','2025-10-31','2025-11-03','2025-11-04']]

class TestCalendar(unittest.TestCase):
    def test_exact_window(self):
        r = audit(S,[D('2025-11-03')],2,2)
        self.assertEqual(r['results'][0]['pre'],('2025-10-30','2025-10-31'))
        self.assertTrue(r['results'][0]['eligible'])
    def test_weekend_boundary(self):
        r = audit(S,[D('2025-11-01')],1,1)
        self.assertEqual(r['results'][0]['post'],('2025-11-03',))
    def test_contamination(self):
        r = audit(S,[D('2025-10-31')],1,2,[D('2025-11-03')])
        self.assertEqual(r['results'][0]['reasons'],('forbidden_session',))
    def test_insufficient(self):
        self.assertEqual(audit(S,[D('2025-10-29')],2,1)['eligible'],0)
    def test_duplicate(self):
        with self.assertRaises(ValueError): audit(S+S[:1],[],1,1)
    def test_invalid_count(self):
        with self.assertRaises(ValueError): audit(S,[],True,1)
    def test_unsorted(self):
        self.assertEqual(audit(list(reversed(S)),[D('2025-11-03')],2,2)['eligible'],1)
    def test_no_candidates(self):
        self.assertEqual(audit(S,[],1,1)['candidates'],0)

if __name__ == '__main__': unittest.main()
