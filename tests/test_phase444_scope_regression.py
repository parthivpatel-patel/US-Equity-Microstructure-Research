"""Constructed-data tests; not historical SEC estimates."""
import sys
from pathlib import Path
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from phase444_scope_regression import compare_scopes

def row(s='AAA', e='X', g='G1', t='1'):
    return dict(security=s, exchange=e, match_group=g, treated=t)

class ScopeTests(unittest.TestCase):
    def test_exchange_specific_group_is_permitted(self):
        r = compare_scopes([row(), row(e='Y', g='G2')])
        self.assertEqual(r['false_positive_security_only_matching_flags'], ['AAA'])
        self.assertEqual(r['within_exchange_matching_conflicts'], [])
    def test_within_exchange_group_change_is_rejected(self):
        r = compare_scopes([row(), row(g='G2')])
        self.assertEqual(r['within_exchange_matching_conflicts'], ['AAA@X'])
        self.assertEqual(r['false_positive_security_only_matching_flags'], [])
    def test_global_treatment_change_detected(self):
        r = compare_scopes([row(), row(e='Y', t='0')])
        self.assertEqual(r['global_treatment_conflicts'], ['AAA'])
    def test_stable_panel(self):
        r = compare_scopes([row(), row(s='BBB', t='0')])
        self.assertEqual(r['security_only_matching_conflicts'], [])
        self.assertEqual(r['global_treatment_conflicts'], [])
    def test_empty_fails(self):
        with self.assertRaises(ValueError): compare_scopes([])
    def test_bad_treatment_fails(self):
        with self.assertRaises(ValueError): compare_scopes([row(t='unknown')])

if __name__ == '__main__': unittest.main()
