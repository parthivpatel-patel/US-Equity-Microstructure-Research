"""Phase 346 regression: zero leave-one-out estimates are not sign reversals.
Synthetic software fixtures only; no authenticated SEC observations.
Run: python -m unittest discover -s tests -p 'test_phase346_zero_sign.py' -v
"""
import importlib.util
import pathlib
import unittest

root = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("phase344", root / "scripts" / "phase344_support_attrition.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def obs(sec, arm, group, numerator):
    return dict(security=sec, date="2025-09-02", exchange="X",
                treated=str(arm), match_group=group,
                numerator=str(numerator), denominator="10")

class ZeroSignRegression(unittest.TestCase):
    def test_positive_baseline_zero_leaveout_not_reversal(self):
        rows = [obs("ta",1,"A",7), obs("ca",0,"A",3),
                obs("tb",1,"B",5), obs("cb",0,"B",5)]
        result = module.analyze(rows)
        self.assertAlmostEqual(result["equal_group_pp"],20)
        self.assertEqual(result["leave_one_group_out"]["sign_reversals"],0)

    def test_negative_baseline_zero_leaveout_not_reversal(self):
        rows = [obs("ta",1,"A",3), obs("ca",0,"A",7),
                obs("tb",1,"B",5), obs("cb",0,"B",5)]
        result = module.analyze(rows)
        self.assertAlmostEqual(result["equal_group_pp"],-20)
        self.assertEqual(result["leave_one_group_out"]["sign_reversals"],0)

    def test_strict_opposite_sign_is_reversal(self):
        rows = [obs("ta",1,"A",9), obs("ca",0,"A",1),
                obs("tb",1,"B",4), obs("cb",0,"B",6)]
        result = module.analyze(rows)
        self.assertAlmostEqual(result["equal_group_pp"],30)
        self.assertEqual(result["leave_one_group_out"]["sign_reversals"],1)

if __name__ == "__main__":
    unittest.main()
