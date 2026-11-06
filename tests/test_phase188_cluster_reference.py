"""Independent covariance reference checks for Phase 187; constructed data only."""
import math
import unittest
from scripts.phase187_cluster import audit

DATES = ("2025-07-01", "2025-07-02", "2025-07-03", "2025-07-07")

def panel(matrix):
    return [
        {"matched_group_id": f"G{i}", "placebo_date": d, "contrast_pp": str(y)}
        for i, row in enumerate(matrix)
        for d, y in zip(DATES, row)
    ]

def reference(matrix):
    """Independent sandwich calculation using intercept OLS score sums."""
    g, t = len(matrix), len(matrix[0])
    n = g * t
    mean = math.fsum(x for row in matrix for x in row) / n
    e = [[x - mean for x in row] for row in matrix]
    scores_g = [math.fsum(row) for row in e]
    scores_t = [math.fsum(e[i][j] for i in range(g)) for j in range(t)]
    # CR1 cluster adjustments, singleton intersections.
    vg = g / (g - 1) * math.fsum(s*s for s in scores_g) / n**2
    vt = t / (t - 1) * math.fsum(s*s for s in scores_t) / n**2
    vi = n / (n - 1) * math.fsum(s*s for row in e for s in row) / n**2
    return mean, vg, vt, vi, vg + vt - vi

class ClusterReferenceTests(unittest.TestCase):
    def test_independent_reference(self):
        matrix = [[1, 3, 2, 6], [4, 1, 7, 3], [2, 8, 5, 9]]
        result = audit(panel(matrix))
        mu, vg, vt, vi, v = reference(matrix)
        for key, expected in (
            ("mean_pp", mu), ("group_component_pp2", vg),
            ("date_component_pp2", vt), ("intersection_component_pp2", vi),
            ("variance_pp2", v)):
            self.assertAlmostEqual(result[key], expected, places=12)

    def test_scaling(self):
        matrix = [[1, 3, 2, 6], [4, 1, 7, 3], [2, 8, 5, 9]]
        a = audit(panel(matrix))
        b = audit(panel([[3*x for x in row] for row in matrix]))
        self.assertAlmostEqual(b["variance_pp2"], 9*a["variance_pp2"], places=12)

    def test_group_and_date_permutation(self):
        matrix = [[1, 3, 2, 6], [4, 1, 7, 3], [2, 8, 5, 9]]
        base = audit(panel(matrix))
        swapped = [matrix[i] for i in (2, 0, 1)]
        self.assertAlmostEqual(base["variance_pp2"], audit(panel(swapped))["variance_pp2"], places=12)
        # Reversing date labels and observations together leaves covariance unchanged.
        rows = panel(matrix)
        mapping = dict(zip(DATES, reversed(DATES)))
        for row in rows:
            row["placebo_date"] = mapping[row["placebo_date"]]
        self.assertAlmostEqual(base["variance_pp2"], audit(rows)["variance_pp2"], places=12)

    def test_no_empirical_claims(self):
        self.assertEqual(len(panel([[1, 2, 3, 4], [5, 6, 7, 8]])), 8)

if __name__ == "__main__":
    unittest.main()
