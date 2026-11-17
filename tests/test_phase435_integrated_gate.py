"""Deterministic constructed-data checks; not empirical SEC validation."""
import unittest
from scripts.phase435_integrated_gate import evaluate

def fixtures():
    daily = {'observations': 8, 'unstable_security_membership': [], 'by_group_exchange': [
        {'match_group': 'A', 'exchange': 'X', 'strict_support': True},
        {'match_group': 'B', 'exchange': 'X', 'strict_support': True}]}
    calendar = {'observations': 8, 'unstable_security_exchange_assignments': [], 'by_unit': [
        {'match_group': g, 'exchange': 'X', 'period': p, 'paired_date_values': [d]}
        for p, d in [('pre', '2025-10-30'), ('post', '2025-11-04')] for g in ('A', 'B')]}
    return daily, calendar

class GateTests(unittest.TestCase):
    def test_valid(self):
        self.assertTrue(evaluate(*fixtures())['pass'])
    def test_one_bad_unit_fails(self):
        a,b=fixtures();a['by_group_exchange'][1]['strict_support']=False
        self.assertFalse(evaluate(a,b)['pass'])
    def test_missing_calendar_unit_fails(self):
        a,b=fixtures();b['by_unit'].pop()
        self.assertFalse(evaluate(a,b)['pass'])
    def test_disjoint_dates_fail(self):
        a,b=fixtures();b['by_unit'][1]['paired_date_values']=['2025-10-31']
        self.assertFalse(evaluate(a,b)['pass'])
    def test_unstable_fails(self):
        a,b=fixtures();a['unstable_security_membership']=['XYZ']
        self.assertFalse(evaluate(a,b)['pass'])
    def test_count_mismatch_fails(self):
        a,b=fixtures();b['observations']=7
        self.assertFalse(evaluate(a,b)['pass'])
    def test_empty_fails(self):
        self.assertFalse(evaluate({'by_group_exchange':[]},{'by_unit':[]})['pass'])
    def test_duplicate_unit_fails(self):
        a,b=fixtures();a['by_group_exchange'].append(dict(a['by_group_exchange'][0]))
        self.assertFalse(evaluate(a,b)['pass'])

if __name__ == '__main__':
    unittest.main()
