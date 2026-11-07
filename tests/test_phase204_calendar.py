import unittest
from phase204_calendar import audit_calendar
E=['2025-11-03','2025-11-04','2025-11-05']
def rows(ds): return [{'date':d,'contrast':1.0} for d in ds]
class CalendarTests(unittest.TestCase):
 def test_complete(self): self.assertTrue(audit_calendar(rows(E),E)['admitted'])
 def test_missing(self): self.assertEqual(audit_calendar(rows(E[:2]),E)['missing_sessions'],[E[2]])
 def test_unexpected(self): self.assertEqual(audit_calendar(rows(E+['2025-11-06']),E)['unexpected_sessions'],['2025-11-06'])
 def test_empty(self): self.assertFalse(audit_calendar([],E)['admitted'])
 def test_duplicate(self):
  with self.assertRaises(ValueError): audit_calendar(rows([E[0],E[0]]),E)
 def test_unsorted(self):
  with self.assertRaises(ValueError): audit_calendar(rows(E[::-1]),E)
 def test_bad_calendar(self):
  with self.assertRaises(ValueError): audit_calendar(rows(E),E[::-1])
 def test_weekend(self):
  with self.assertRaises(ValueError): audit_calendar(rows(['2025-11-08']),['2025-11-08'])
 def test_nonfinite(self):
  with self.assertRaises(ValueError): audit_calendar([{'date':E[0],'contrast':float('nan')}],E)
 def test_not_authenticated(self): self.assertFalse(audit_calendar(rows(E),E)['calendar_authenticated'])
if __name__=='__main__': unittest.main()
