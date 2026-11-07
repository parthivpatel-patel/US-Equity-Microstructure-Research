"""Integration tests requiring the exact phase224 and phase225 repository modules."""
import unittest
from phase226_matched_hac_bridge import matched_full_series_hac

DATES=['2025-09-02','2025-09-03','2025-09-04','2025-09-05']
def fixture():
    return [dict(date=d,security=s,exchange='X',
                 hidden_count=(2+i if s=='T' else 1),total_count=10)
            for i,d in enumerate(DATES) for s in ('T','C')]

class BridgeTests(unittest.TestCase):
    def calc(self, **kw):
        args=dict(rows=fixture(),pairs=[('T','C')],sessions=DATES,exchanges=['X'],
                  early_dates=DATES[:2],late_dates=DATES[2:],bandwidth=1)
        args.update(kw)
        return matched_full_series_hac(**args)
    def test_known_difference(self):
        r=self.calc()
        self.assertAlmostEqual(r['equal_cell_contrast']['difference'],.2)
        self.assertFalse(r['source_authenticated'])
        self.assertFalse(r['security_cluster_inference'])
    def test_order_invariance(self):
        self.assertEqual(self.calc(),self.calc(rows=list(reversed(fixture()))))
    def test_missing_cell_rejected(self):
        with self.assertRaises(ValueError): self.calc(rows=fixture()[:-1])
    def test_duplicate_rejected(self):
        with self.assertRaises(ValueError): self.calc(rows=fixture()+fixture()[:1])
    def test_window_mismatch_rejected(self):
        with self.assertRaises(ValueError): self.calc(late_dates=DATES[1:])
    def test_bandwidth_rejected(self):
        with self.assertRaises(ValueError): self.calc(bandwidth=4)
    def test_variance_nonnegative(self):
        self.assertGreaterEqual(self.calc()['equal_cell_contrast']['hac_variance'],0)

if __name__=='__main__': unittest.main()
