"""Deterministic constructed-data tests; no SEC estimates."""
import unittest
from scripts.phase187_cluster import audit
def fixture():
    return [dict(matched_group_id=g,placebo_date=d,contrast_pp=str(y))
      for g,vals in [('A',[1,2,3]),('B',[2,4,6]),('C',[3,6,9])]
      for d,y in zip(['2025-07-01','2025-07-02','2025-07-03'],vals)]
class ClusterTests(unittest.TestCase):
    def test_balanced(self):
        a=audit(fixture());self.assertEqual((a['groups'],a['dates'],a['observations']),(3,3,9))
        self.assertAlmostEqual(a['mean_pp'],4)
        self.assertAlmostEqual(a['variance_pp2'],a['group_component_pp2']+a['date_component_pp2']-a['intersection_component_pp2'])
    def test_translation(self):
        a=audit(fixture());b=fixture()
        for r in b:r['contrast_pp']=str(float(r['contrast_pp'])+10)
        self.assertAlmostEqual(a['variance_pp2'],audit(b)['variance_pp2'])
    def test_permutation(self):self.assertEqual(audit(fixture()),audit(list(reversed(fixture()))))
    def test_duplicate(self):
        with self.assertRaisesRegex(ValueError,'duplicate'):audit(fixture()+fixture()[:1])
    def test_unbalanced(self):
        with self.assertRaisesRegex(ValueError,'unbalanced'):audit(fixture()[:-1])
    def test_bad_date(self):
        a=fixture();a[0]['placebo_date']='2025-02-30'
        with self.assertRaisesRegex(ValueError,'date'):audit(a)
    def test_nonfinite(self):
        a=fixture();a[0]['contrast_pp']='nan'
        with self.assertRaisesRegex(ValueError,'nonfinite'):audit(a)
    def test_single_cluster(self):
        with self.assertRaisesRegex(ValueError,'at least two'):audit(fixture()[:3])
    def test_schema(self):
        a=fixture();a[0]['extra']='x'
        with self.assertRaisesRegex(ValueError,'schema'):audit(a)
    def test_constant(self):
        a=fixture()
        for r in a:r['contrast_pp']='2'
        self.assertEqual(audit(a)['standard_error_pp'],0)
if __name__=='__main__':unittest.main()
