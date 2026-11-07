import unittest
from scripts.phase223_weight_sensitivity import weighting_sensitivity

DAYS=['2025-10-01','2025-10-02']

def fixture():
    rows=[]
    for day in DAYS:
        for s in ('T','C'):
            for e in ('X','Y'):
                h,n = ((9,10) if e=='X' else (10,100)) if s=='T' else ((4,10) if e=='X' else (40,100))
                rows.append(dict(date=day,security=s,exchange=e,hidden_count=h,total_count=n))
    return rows

class WeightSensitivityTests(unittest.TestCase):
    def run_model(self, rows=None):
        return weighting_sensitivity(fixture() if rows is None else rows,DAYS,['T'],['C'],['X','Y'])
    def test_weighting_can_reverse_sign(self):
        x=self.run_model()['daily'][0]
        self.assertAlmostEqual(x['equal_cell_contrast'],.1)
        self.assertAlmostEqual(x['pooled_count_contrast'],19/110-44/110)
        self.assertGreater(x['equal_cell_contrast'],0)
        self.assertLess(x['pooled_count_contrast'],0)
    def test_two_days(self):
        self.assertEqual(len(self.run_model()['daily']),2)
    def test_permutation_invariant(self):
        self.assertEqual(self.run_model()['daily'],self.run_model(list(reversed(fixture())))['daily'])
    def test_missing_cell_fails(self):
        with self.assertRaisesRegex(ValueError,'incomplete'):self.run_model(fixture()[:-1])
    def test_duplicate_cell_fails(self):
        rows=fixture();rows.append(dict(rows[0]))
        with self.assertRaisesRegex(ValueError,'duplicate'):self.run_model(rows)
    def test_no_authentication_claim(self):
        self.assertFalse(self.run_model()['admission']['source_authenticated'])

if __name__=='__main__':unittest.main()
