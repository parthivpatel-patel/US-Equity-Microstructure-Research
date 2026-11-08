import unittest
from phase236_window_guard import validate_estimation_windows as guard
C=['2025-09-02','2025-09-03','2025-09-04','2025-09-05']
class TestWindowGuard(unittest.TestCase):
    def call(self, sessions=C, early=C[:2], late=C[2:], calendar=C):
        return guard(sessions, early, late, calendar)
    def test_valid(self):
        self.assertEqual(self.call()['n_sessions'],4)
        self.assertFalse(self.call()['calendar_independently_verified'])
    def test_empty_early(self):
        with self.assertRaises(ValueError): self.call(early=[])
    def test_empty_late(self):
        with self.assertRaises(ValueError): self.call(late=[])
    def test_noncanonical_date(self):
        with self.assertRaises(ValueError): self.call(sessions=['2025-9-02']+C[1:])
    def test_duplicate(self):
        with self.assertRaises(ValueError): self.call(sessions=[C[0],C[0]]+C[2:])
    def test_overlap(self):
        with self.assertRaises(ValueError): self.call(early=C[:3],late=C[2:])
    def test_missing_calendar_session(self):
        with self.assertRaises(ValueError): self.call(calendar=C[:3])
    def test_unsorted_calendar(self):
        with self.assertRaises(ValueError): self.call(calendar=C[::-1])
    def test_wrong_partition(self):
        with self.assertRaises(ValueError): self.call(early=C[:1],late=C[2:])
    def test_nonstring(self):
        with self.assertRaises(ValueError): self.call(sessions=[20250902]+C[1:])
    def test_malformed(self):
        with self.assertRaises(ValueError): self.call(sessions=['2025-09-99']+C[1:])
if __name__=='__main__': unittest.main()
