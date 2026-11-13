import unittest
from scripts.phase341_support import audit
def row(s,d,e,t,g='G'):
    return dict(security=s,date=d,exchange=e,treated=t,match_group=g)
class Tests(unittest.TestCase):
    def test_full_overlap(self):
        r=audit([row('T','2025-10-01','X','1'),row('C','2025-10-01','X','0')]); self.assertEqual(r['groups'][0]['paired_dates'],1); self.assertEqual(r['group_exchange_support'][0]['paired_dates'],1)
    def test_disjoint_dates(self):
        r=audit([row('T','2025-10-01','X','1'),row('C','2025-10-02','X','0')]); self.assertEqual(r['zero_paired_groups'],['G'])
    def test_disjoint_exchanges(self):
        r=audit([row('T','2025-10-01','X','1'),row('C','2025-10-01','Y','0')]); self.assertEqual(r['groups'][0]['paired_dates'],1); self.assertTrue(all(x['paired_dates']==0 for x in r['group_exchange_support']))
    def test_duplicate(self):
        with self.assertRaises(ValueError): audit([row('T','2025-10-01','X','1')]*2)
    def test_drift(self):
        with self.assertRaises(ValueError): audit([row('T','2025-10-01','X','1'),row('T','2025-10-02','X','0')])
    def test_invalid_date(self):
        with self.assertRaises(ValueError): audit([row('T','2025-02-30','X','1')])
    def test_empty(self):
        with self.assertRaises(ValueError): audit([])
    def test_missing_field(self):
        with self.assertRaises(ValueError): audit([{'security':'T'}])
if __name__=='__main__': unittest.main()
