import unittest
from scripts.phase422_panel_membership import audit
def r(date='2025-09-02',security='A',exchange='X',match_group='G',treated='1',hidden_count='2',total_count='10'):
    return dict(date=date,security=security,exchange=exchange,match_group=match_group,treated=treated,hidden_count=hidden_count,total_count=total_count)
class Tests(unittest.TestCase):
    def test_paired(self): self.assertTrue(audit([r(),r(security='B',treated='0')])['structural_pass'])
    def test_switch(self): self.assertEqual(audit([r(),r(security='B',treated='0'),r(date='2025-09-03',treated='0')])['unstable_security_membership'],['A'])
    def test_group_switch(self): self.assertEqual(audit([r(),r(security='B',treated='0'),r(date='2025-09-03',match_group='H')])['unstable_security_membership'],['A'])
    def test_unpaired(self): self.assertEqual(audit([r()])['groups_missing_arm'],['G'])
    def test_weekend(self):
        with self.assertRaises(ValueError): audit([r(date='2025-09-06')])
    def test_duplicate(self):
        with self.assertRaises(ValueError): audit([r(),r()])
    def test_bad_count(self):
        with self.assertRaises(ValueError): audit([r(hidden_count='11')])
    def test_empty(self):
        with self.assertRaises(ValueError): audit([])
    def test_post(self):
        with self.assertRaises(ValueError): audit([r(date='2025-11-03')])
    def test_multi_exchange(self): self.assertTrue(audit([r(),r(security='B',treated='0'),r(exchange='Y'),r(security='B',treated='0',exchange='Y')])['structural_pass'])
if __name__=='__main__': unittest.main()
