import unittest
from phase195_support import audit

def pair(w, d, s="A", e="X"):
    return [dict(window=w, date=d, security=s, exchange=e, group="G",
                 outcome=o, value=1.0) for o in ("count", "volume")]

class SupportTests(unittest.TestCase):
    def test_disjoint_same_units(self):
        x = audit(pair("pre", "2025-10-01") + pair("post", "2025-11-03"))
        self.assertTrue(x["structurally_valid"])
        self.assertTrue(x["cross_window"][0]["identical_units"])
        self.assertEqual(x["cross_window"][0]["shared_dates"], 0)

    def test_different_security(self):
        x = audit(pair("pre", "2025-10-01") + pair("post", "2025-11-03", "B"))
        self.assertFalse(x["cross_window"][0]["identical_units"])

    def test_different_exchange(self):
        x = audit(pair("pre", "2025-10-01") + pair("post", "2025-11-03", e="Y"))
        self.assertFalse(x["cross_window"][0]["identical_units"])

    def test_incomplete(self):
        self.assertFalse(audit(pair("pre", "2025-10-01")[:1])["structurally_valid"])

    def test_drift(self):
        x = audit(pair("pre", "2025-10-01") + pair("pre", "2025-10-02", "B"))
        self.assertEqual(len(x["roster_drift_dates"]["pre"]), 2)

    def test_duplicate(self):
        p = pair("pre", "2025-10-01")
        with self.assertRaisesRegex(ValueError, "duplicate"):
            audit(p + [p[0]])

    def test_weekend(self):
        with self.assertRaisesRegex(ValueError, "weekend"):
            audit(pair("pre", "2025-10-04"))

    def test_nan(self):
        p = pair("pre", "2025-10-01")
        p[0]["value"] = float("nan")
        with self.assertRaisesRegex(ValueError, "nonfinite"):
            audit(p)

    def test_empty(self):
        with self.assertRaisesRegex(ValueError, "empty"):
            audit([])

    def test_missing(self):
        with self.assertRaisesRegex(ValueError, "missing"):
            audit([{"window": "pre"}])

if __name__ == "__main__":
    unittest.main()
