"""Adversarial cross-window covariance checks; constructed values only."""
import unittest

def variance(values, split, lag):
    n = len(values)
    assert 0 < split < n and 0 <= lag < n
    early = sum(values[:split]) / split
    late = sum(values[split:]) / (n - split)
    scores = [-(v - early) / split for v in values[:split]]
    scores += [(v - late) / (n - split) for v in values[split:]]
    base = sum(s*s for s in scores)
    full = base
    blocked = base
    for k in range(1, lag + 1):
        weight = 2 * (1 - k / (lag + 1))
        for t in range(k, n):
            term = weight * scores[t] * scores[t-k]
            full += term
            if (t < split) == (t-k < split):
                blocked += term
    return full, blocked

class CrossWindowCovarianceTests(unittest.TestCase):
    def setUp(self):
        self.values = [1, 3, 2, 4, 5, 7, 6, 8, 9, 11]

    def test_zero_lag_same(self):
        a, b = variance(self.values, 5, 0)
        self.assertAlmostEqual(a, 0.992)
        self.assertAlmostEqual(a, b)

    def test_lag_one_cross_boundary(self):
        a, b = variance(self.values, 5, 1)
        self.assertAlmostEqual(a, 1.3344)
        self.assertAlmostEqual(b, 1.2384)
        self.assertAlmostEqual(a-b, 0.096)

    def test_lag_three_cross_boundary(self):
        a, b = variance(self.values, 5, 3)
        self.assertAlmostEqual(a, 1.492)
        self.assertAlmostEqual(b, 1.096)

    def test_lag_five_cross_boundary(self):
        a, b = variance(self.values, 5, 5)
        self.assertAlmostEqual(a, 1.029333333333333)
        self.assertAlmostEqual(b, 0.730666666666667)

if __name__ == "__main__":
    unittest.main()
