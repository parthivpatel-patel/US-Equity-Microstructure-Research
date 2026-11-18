import unittest
from phase448_calendar_support import audit

def pair(d, group='A', exchange='X'):
    return [dict(date=d, security=s, exchange=exchange, matched_group=group, treated=t)
            for s, t in [('T', True), ('C', False)]]

class SupportTests(unittest.TestCase):
    def test_supported(self):
        rows = sum((pair(d) for d in ['2025-09-01', '2025-09-02', '2025-10-01', '2025-10-02', '2025-11-03', '2025-11-04']), [])
        result = audit(rows)
        self.assertTrue(result['all_strata_placebo_supported'])
        self.assertTrue(result['all_strata_reform_supported'])
        self.assertEqual(result['strata'][0]['september_common_dates'], 2)
    def test_unmatched_day_excluded(self):
        rows = pair('2025-09-01') + [dict(date='2025-10-01', security='T', exchange='X', matched_group='A', treated=True)]
        self.assertEqual(audit(rows)['strata'][0]['common_dates'], 1)
    def test_no_post_support(self):
        self.assertFalse(audit(pair('2025-09-01'))['all_strata_reform_supported'])
    def test_duplicate_rejected(self):
        with self.assertRaises(ValueError): audit(pair('2025-09-01') * 2)
    def test_empty_rejected(self):
        with self.assertRaises(ValueError): audit([])
    def test_bad_treatment_rejected(self):
        rows = pair('2025-09-01'); rows[0]['treated'] = 1
        with self.assertRaises(ValueError): audit(rows)
    def test_bad_date_rejected(self):
        with self.assertRaises(ValueError): audit(pair('2025-09-99'))
    def test_strata_separate(self):
        rows = pair('2025-09-01', 'A') + pair('2025-10-01', 'B')
        self.assertEqual(len(audit(rows)['strata']), 2)
        self.assertTrue(all(x['common_dates'] == 1 for x in audit(rows)['strata']))
    def test_bad_placebo_order(self):
        with self.assertRaises(ValueError): audit(pair('2025-09-01'), placebo_date='2025-12-01')
    def test_bad_identifier(self):
        rows = pair('2025-09-01'); rows[0]['exchange'] = ''
        with self.assertRaises(ValueError): audit(rows)

if __name__ == '__main__': unittest.main()
