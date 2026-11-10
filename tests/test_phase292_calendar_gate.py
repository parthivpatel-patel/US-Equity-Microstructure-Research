"""Synthetic regression checks; no SEC observations or authenticated calendars."""
import unittest
from phase292_calendar_gate import canonical_day, admit_calendar, calendar_gated_bootstrap

PANEL = {'source_authenticated': False, 'pair_counts_by_exchange': {'X': 2}, 'dates': [
    {'date':'2025-11-03','by_exchange':{'X':1.0}},
    {'date':'2025-11-04','by_exchange':{'X':3.0}}]}
CAL = ['2025-11-03','2025-11-04']

class CalendarGateTests(unittest.TestCase):
    def test_valid(self): self.assertEqual(admit_calendar(PANEL,CAL), PANEL)
    def test_integrated(self):
        result = calendar_gated_bootstrap(PANEL,CAL,repetitions=20,seed=1,block_length=2)
        self.assertEqual(result['mean'],2.0)
        self.assertFalse(result['causal_inference_authorized'])
    def test_missing(self):
        with self.assertRaises(ValueError): admit_calendar(PANEL,CAL+['2025-11-05'])
    def test_extra(self):
        with self.assertRaises(ValueError): admit_calendar(PANEL,CAL[:1])
    def test_unsorted(self):
        with self.assertRaises(ValueError): admit_calendar(PANEL,CAL[::-1])
    def test_duplicate(self):
        with self.assertRaises(ValueError): admit_calendar(PANEL,CAL+[CAL[-1]])
    def test_impossible(self):
        with self.assertRaises(ValueError): canonical_day('2025-02-29')
    def test_unicode(self):
        with self.assertRaises(ValueError): canonical_day('２０２５-11-03')
    def test_bad_provenance(self):
        with self.assertRaises(ValueError): admit_calendar({**PANEL,'source_authenticated':True},CAL)
    def test_empty(self):
        with self.assertRaises(ValueError): admit_calendar(PANEL,[])
    def test_no_rows(self):
        with self.assertRaises(ValueError): admit_calendar({**PANEL,'dates':None},CAL)
    def test_incomplete_exchange_rejected_by_delegate(self):
        bad={**PANEL,'dates':[PANEL['dates'][0],{'date':'2025-11-04','by_exchange':{}}]}
        with self.assertRaises(ValueError): calendar_gated_bootstrap(bad,CAL,repetitions=20,block_length=2)

if __name__ == '__main__': unittest.main()
