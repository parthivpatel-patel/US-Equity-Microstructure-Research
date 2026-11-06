"""Deterministic tests on constructed observations, not SEC estimates."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from phase192_pairing_gate import audit

def row(day, group, outcome, security='S', exchange='X', contrast='1'):
    return dict(security_id=security, exchange=exchange, trade_date=day,
                matched_group_id=group, outcome=outcome, contrast_pp=contrast)

class PairingTests(unittest.TestCase):
    def test_stable_complete(self):
        rows = [row(d, g, o) for d in ('2025-10-06', '2025-10-07')
                for g in ('A', 'B') for o in ('count', 'volume')]
        result = audit(rows)
        self.assertTrue(result['eligible_for_fixed_roster_common_date_analysis'])
        self.assertEqual(result['common_units'], 2)

    def test_missing_outcome(self):
        rows = [row('2025-10-06', 'A', 'count'), row('2025-10-07', 'A', 'count'),
                row('2025-10-07', 'A', 'volume')]
        self.assertEqual(audit(rows)['unpaired_unit_dates'], 1)

    def test_equal_counts_different_roster(self):
        rows = [row(d, g, o) for d, g in [('2025-10-06', 'A'), ('2025-10-07', 'B')]
                for o in ('count', 'volume')]
        result = audit(rows)
        self.assertFalse(result['roster_stable'])
        self.assertEqual(result['common_units'], 0)

    def test_duplicate(self):
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            audit([row('2025-10-06', 'A', 'count')] * 2)

    def test_nonfinite(self):
        with self.assertRaisesRegex(ValueError, 'invalid date or contrast'):
            audit([row('2025-10-06', 'A', 'count', contrast='nan')])

    def test_weekend(self):
        with self.assertRaisesRegex(ValueError, 'invalid date or contrast'):
            audit([row('2025-10-05', 'A', 'count')])

    def test_empty(self):
        with self.assertRaisesRegex(ValueError, 'empty panel'):
            audit([])

if __name__ == '__main__':
    unittest.main()
