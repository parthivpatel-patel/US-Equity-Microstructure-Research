import unittest
from scripts.phase304_panel_key_audit import audit_panel_keys

def row(security='A', date='2025-09-02', exchange='X'):
    return {'security': security, 'date': date, 'exchange': exchange}

class PanelKeyAuditTests(unittest.TestCase):
    def test_same_date_multiple_securities_and_exchanges_allowed(self):
        result = audit_panel_keys([row(), row('B'), row('A', exchange='Y')], ['2025-09-02'])
        self.assertTrue(result['structurally_consistent'])
        self.assertEqual(result['n_security_exchange_pairs'], 3)
    def test_duplicate_triplet_flagged(self):
        result = audit_panel_keys([row(), row()])
        self.assertFalse(result['structurally_consistent'])
        self.assertEqual(result['duplicate_keys'][0]['count'], 2)
    def test_missing_date_is_pair_specific(self):
        result = audit_panel_keys([row(), row('B', '2025-09-03')], ['2025-09-02', '2025-09-03'])
        self.assertEqual(len(result['missing_pair_dates']), 2)
        self.assertFalse(result['structurally_consistent'])
    def test_extra_date(self):
        result = audit_panel_keys([row()], ['2025-09-03'])
        self.assertEqual(len(result['unexpected_pair_dates']), 1)
    def test_no_calendar_does_not_claim_authentication(self):
        result = audit_panel_keys([row()])
        self.assertFalse(result['source_authenticated'])
        self.assertFalse(result['panel_universe_authenticated'])
    def test_reject_weekend(self):
        with self.assertRaises(ValueError):
            audit_panel_keys([row(date='2025-09-06')])
    def test_reject_bad_identifiers(self):
        for identifier in ('', ' A ', None, 5):
            with self.subTest(identifier=identifier), self.assertRaises(ValueError):
                audit_panel_keys([row(security=identifier)])
    def test_reject_duplicate_calendar(self):
        with self.assertRaises(ValueError):
            audit_panel_keys([row()], ['2025-09-02', '2025-09-02'])
    def test_reject_empty_rows(self):
        with self.assertRaises(ValueError):
            audit_panel_keys([])

if __name__ == '__main__':
    unittest.main()
