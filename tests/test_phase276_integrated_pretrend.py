"""Deterministic synthetic tests; never represent SEC historical findings."""
import unittest
from phase276_integrated_pretrend import evaluate_admitted

C = ['2025-09-02', '2025-09-03', '2025-09-04', '2025-09-05', '2025-09-08']
E = ('2025-09-02', '2025-09-03')
L = ('2025-09-05', '2025-09-08')

def rows():
    return list(zip(C, [1., 2., 3., 4., 7.]))

class IntegrationTests(unittest.TestCase):
    def test_valid_gap_is_reported(self):
        r = evaluate_admitted(iter(C), iter(rows()), E, L)
        self.assertEqual(r['admission']['gap_sessions'], 1)
        self.assertAlmostEqual(r['descriptive_pretrend']['late_minus_early_mean'], 4.)
        self.assertFalse(r['historical_inference_authorized'])
    def test_gap_rejected_when_partition_required(self):
        with self.assertRaises(ValueError):
            evaluate_admitted(C, rows(), E, L, require_contiguous_partition=True)
    def test_contiguous_partition(self):
        r = evaluate_admitted(C, rows(), ('2025-09-02','2025-09-04'), ('2025-09-05','2025-09-08'), require_contiguous_partition=True)
        self.assertEqual(r['admission']['gap_sessions'], 0)
    def test_missing_observation(self):
        with self.assertRaises(ValueError): evaluate_admitted(C, rows()[:-1], E, L)
    def test_duplicate_observation(self):
        with self.assertRaises(ValueError): evaluate_admitted(C, rows()[:-1]+[rows()[0]], E, L)
    def test_missing_endpoint(self):
        with self.assertRaises(ValueError): evaluate_admitted(C, rows(), ('2025-09-01','2025-09-03'), L)
    def test_unsorted_calendar(self):
        with self.assertRaises(ValueError): evaluate_admitted(C[::-1], rows(), E, L)
    def test_nonfinite(self):
        r = rows(); r[2] = (r[2][0], float('nan'))
        with self.assertRaises(ValueError): evaluate_admitted(C, r, E, L)
    def test_no_authentication_claim(self):
        r = evaluate_admitted(C, rows(), E, L)
        for k in ('source_authenticated','calendar_authenticated','treatment_authenticated','historical_inference_authorized'):
            self.assertIs(r[k], False)

if __name__ == '__main__': unittest.main()
