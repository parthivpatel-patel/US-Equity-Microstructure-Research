"""Constructed fixtures only; no historical market data."""
import unittest
from scripts.phase423_pairing_coverage import audit
def row(day='2025-09-02',security='A',arm='1',group='G',exchange='X',hidden='1',total='2'):
    return dict(date=day,security=security,treated=arm,match_group=group,exchange=exchange,hidden_count=hidden,total_count=total)
class PairingTests(unittest.TestCase):
    def test_paired(self):self.assertEqual(audit([row(),row(security='B',arm='0')])['paired_cells'],1)
    def test_global_group_not_date_paired(self):self.assertEqual(audit([row(),row(day='2025-09-03',security='B',arm='0')])['paired_cells'],0)
    def test_cross_exchange_not_paired(self):self.assertEqual(audit([row(),row(security='B',arm='0',exchange='Y')])['paired_cells'],0)
    def test_missing_dates(self):self.assertEqual(audit([row()])['dates_without_pairs'],['2025-09-02'])
    def test_membership_change(self):self.assertEqual(audit([row(),row(day='2025-09-03',arm='0')])['unstable_security_membership'],['A'])
    def test_duplicate(self):
        with self.assertRaises(ValueError):audit([row(),row()])
    def test_invalid_counts(self):
        with self.assertRaises(ValueError):audit([row(hidden='3')])
    def test_weekend(self):
        with self.assertRaises(ValueError):audit([row(day='2025-09-06')])
    def test_three_dates(self):
        rows=[]
        for day in ('2025-09-02','2025-09-03','2025-09-04'):
            rows.extend([row(day=day),row(day=day,security='B',arm='0')])
        self.assertTrue(audit(rows)['estimation_ready'])
    def test_empty(self):
        with self.assertRaises(ValueError):audit([])
if __name__=='__main__':unittest.main()
