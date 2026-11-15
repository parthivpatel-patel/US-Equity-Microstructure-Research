import unittest
from fractions import Fraction
from phase380_roster_attrition import audit_roster_attrition

class RosterAuditTests(unittest.TestCase):
    def setUp(self):
        self.roster = [('p1', 'X'), ('p2', 'Y')]
        self.rows = [(p, d, e, a, 1, 2) for p, e in self.roster for d in ('pre', 'post') for a in ('T', 'C')]
    def test_complete(self):
        r = audit_roster_attrition(self.rows, self.roster, ['pre'], ['post'])
        self.assertEqual(r['expected_rows'], 8)
        self.assertEqual(r['by_exchange']['X']['retention'], Fraction(1))
    def test_missing(self):
        r = audit_roster_attrition(self.rows[:-1], self.roster, ['pre'], ['post'])
        self.assertEqual(r['by_exchange']['Y']['retention'], Fraction(0))
        self.assertEqual(len(r['missing_keys']), 1)
    def test_no_false_cross_product(self):
        self.assertEqual(audit_roster_attrition(self.rows, self.roster, ['pre'], ['post'])['expected_rows'], 8)
    def test_unexpected_exchange_rejected(self):
        with self.assertRaises(ValueError):
            audit_roster_attrition(self.rows + [('p1', 'pre', 'Y', 'T', 1, 2)], self.roster, ['pre'], ['post'])
    def test_duplicate_roster_rejected(self):
        with self.assertRaises(ValueError):
            audit_roster_attrition(self.rows, self.roster + [self.roster[0]], ['pre'], ['post'])
    def test_invalid_count_rejected(self):
        with self.assertRaises(ValueError):
            audit_roster_attrition(self.rows[:-1] + [('p2', 'post', 'Y', 'C', 3, 2)], self.roster, ['pre'], ['post'])
    def test_duplicate_row_rejected(self):
        with self.assertRaises(ValueError):
            audit_roster_attrition(self.rows + [self.rows[0]], self.roster, ['pre'], ['post'])
if __name__ == '__main__':
    unittest.main()
