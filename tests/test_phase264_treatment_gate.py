import unittest
from scripts.phase264_treatment_gate import audit
R = [("p1", "AAA", "X", "treated"), ("p1", "BBB", "X", "control")]
D = ["2025-10-06", "2025-10-07"]
def obs(r=R, d=D):
    return [(date, *entry, 1.0) for date in d for entry in r]
class Tests(unittest.TestCase):
    def test_complete(self): self.assertTrue(audit(R, obs(), D)["passed"])
    def test_no_auth(self): self.assertFalse(audit(R, obs(), D)["authenticated"])
    def test_missing_arm(self): self.assertIn("unbalanced_pair", audit(R[:1], obs(R[:1]), D)["problems"])
    def test_missing_cell(self): self.assertIn("missing_observation", audit(R, obs()[:-1], D)["problems"])
    def test_extra_cell(self): self.assertIn("unexpected_observation", audit(R, obs() + [("2025-10-08", *R[0], 1)], D)["problems"])
    def test_duplicate(self): self.assertIn("duplicate_observation", audit(R, obs() + obs()[:1], D)["problems"])
    def test_reused_security(self):
        r = R + [("p2", "AAA", "X", "treated"), ("p2", "CCC", "X", "control")]
        self.assertIn("security_exchange_reused", audit(r, obs(r), D)["problems"])
    def test_invalid_arm(self):
        r = [("p1", "AAA", "X", "treatment"), R[1]]
        self.assertIn("invalid_arm", audit(r, obs(r), D)["problems"])
    def test_nan(self):
        o = obs(); o[0] = (*o[0][:-1], float("nan"))
        self.assertIn("invalid_outcome", audit(R, o, D)["problems"])
    def test_duplicate_calendar(self): self.assertIn("invalid_calendar", audit(R, obs(), D + D[:1])["problems"])
if __name__ == "__main__": unittest.main()
