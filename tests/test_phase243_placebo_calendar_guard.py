import unittest
from phase243_placebo_calendar_guard import validate_placebo_sessions as check

class GuardTests(unittest.TestCase):
    def setUp(self):
        self.rows = [{'date': d} for d in ['2025-10-06','2025-10-07','2025-10-08','2025-10-09','2025-10-10','2025-10-13']]
    def test_valid(self):
        self.assertEqual(check(self.rows,[2,3,4],2)['n_cuts'],3)
        self.assertFalse(check(self.rows,[2],2)['calendar_independently_verified'])
    def test_weekend(self):
        self.rows[0]['date']='2025-10-05'
        with self.assertRaises(ValueError): check(self.rows,[2],2)
    def test_invalid_calendar_date(self):
        self.rows[0]['date']='2025-02-30'
        with self.assertRaises(ValueError): check(self.rows,[2],2)
    def test_noncanonical(self):
        self.rows[0]['date']='20251006'
        with self.assertRaises(ValueError): check(self.rows,[2],2)
    def test_duplicates(self):
        self.rows[1]['date']=self.rows[0]['date']
        with self.assertRaises(ValueError): check(self.rows,[2],2)
    def test_unsorted(self):
        with self.assertRaises(ValueError): check(self.rows[::-1],[2],2)
    def test_missing_window(self):
        with self.assertRaises(ValueError): check(self.rows,[5],2)
    def test_duplicate_cut(self):
        with self.assertRaises(ValueError): check(self.rows,[2,2],2)
    def test_boolean_cut(self):
        with self.assertRaises(ValueError): check(self.rows,[True],2)
    def test_not_authenticated_even_when_weekdays(self):
        rows=[{'date':d} for d in ['2025-08-28','2025-08-29','2025-09-01','2025-09-02']]
        self.assertFalse(check(rows,[2],2)['calendar_independently_verified'])

if __name__ == '__main__': unittest.main()
