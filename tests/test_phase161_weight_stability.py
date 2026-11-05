"""Stable group-weight concentration diagnostics. Constructed fixtures only."""
import math
import unittest

def weight_diagnostics(weights):
    if not weights:
        raise ValueError("empty weights")
    if any(type(w) not in (int, float) or not math.isfinite(w) or w <= 0 for w in weights):
        raise ValueError("weights must be positive finite numbers")
    scale = max(weights)
    normalized = [w / scale for w in weights]
    total = math.fsum(normalized)
    squared = math.fsum(w*w for w in normalized)
    if not squared or not math.isfinite(total):
        raise ValueError("numerically degenerate weights")
    ess = total*total/squared
    return {"n": len(weights), "ess": ess, "ess_fraction": ess/len(weights),
            "largest_weight_share": 1/total, "herfindahl": squared/(total*total)}

class WeightTests(unittest.TestCase):
    def test_equal_weights(self):
        r=weight_diagnostics([5]*20)
        self.assertAlmostEqual(r["ess"],20)
        self.assertAlmostEqual(r["largest_weight_share"],.05)
    def test_concentrated_weights(self):
        r=weight_diagnostics([100,1])
        self.assertAlmostEqual(r["ess"],10201/10001)
        self.assertAlmostEqual(r["largest_weight_share"],100/101)
    def test_scaling_invariance(self):
        a=weight_diagnostics([2,3,7]); b=weight_diagnostics([2e150,3e150,7e150])
        self.assertAlmostEqual(a["ess"],b["ess"])
    def test_large_values_no_overflow(self):
        self.assertAlmostEqual(weight_diagnostics([1e300,1e300])["ess"],2)
    def test_reject_invalid(self):
        for w in ([],[0,1],[-1,2],[float("nan")],[float("inf")],[True,1],["1",2]):
            with self.subTest(w=w), self.assertRaises(ValueError):
                weight_diagnostics(w)
    def test_ess_bounds(self):
        for weights in ([1,2,3],[1,1,100],[5],[1e-200,1]):
            r=weight_diagnostics(weights)
            self.assertGreaterEqual(r["ess"],1-1e-12)
            self.assertLessEqual(r["ess"],len(weights)+1e-12)
    def test_herfindahl_identity(self):
        r=weight_diagnostics([4,5,8])
        self.assertAlmostEqual(r["ess"]*r["herfindahl"],1)

if __name__=="__main__":
    unittest.main()
