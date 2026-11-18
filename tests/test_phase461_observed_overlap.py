import unittest
from phase461_observed_overlap import observed_overlap


def fixture():
    out = []
    for d in ("2025-08-29", "2025-09-02", "2025-09-30", "2025-10-01", "2025-10-02", "2025-10-31"):
        for s, t in (("T", True), ("C", False)):
            out.append(dict(security=s, exchange="X", matched_group="G", date=d,
                            treated=t, outcome=1.0 if t else 0.0))
    return out


class OverlapTests(unittest.TestCase):
    def test_observed_reassignment(self):
        x = observed_overlap(fixture(), ["2025-09-01", "2025-10-01"], min_pre=1)
        self.assertEqual(x["comparisons"][0]["reassigned_observed_dates"], 2)
        self.assertEqual(x["comparisons"][0]["shared_pre_dates"], 1)
        self.assertEqual(x["comparisons"][0]["shared_post_dates"], 3)
    def test_minimum_support(self):
        x = observed_overlap(fixture(), ["2025-09-01", "2025-10-01"])
        self.assertEqual(x["windows"][0]["eligible_groups"], 0)
        self.assertEqual(x["common_groups_all_boundaries"], 0)
    def test_relaxed_support(self):
        x = observed_overlap(fixture(), ["2025-09-01", "2025-10-01"], min_pre=1)
        self.assertEqual(x["common_groups_all_boundaries"], 1)
    def test_duplicate_rejected(self):
        r = fixture()
        with self.assertRaises(ValueError): observed_overlap(r + [r[0]], ["2025-10-01"])
    def test_cross_exchange_conflict(self):
        r = fixture() + [dict(security="T", exchange="Y", matched_group="G", date="2025-09-01", treated=False, outcome=0.)]
        with self.assertRaises(ValueError): observed_overlap(r, ["2025-10-01"])
    def test_unpaired_cells(self):
        r = fixture() + [dict(security="T", exchange="X", matched_group="G", date="2025-10-30", treated=True, outcome=1.)]
        self.assertEqual(observed_overlap(r, ["2025-10-01"])["unpaired_group_date_cells"], 1)
    def test_invalid_cut(self):
        with self.assertRaises(ValueError): observed_overlap(fixture(), ["2025-11-03"])
    def test_nonfinite(self):
        r = fixture(); r[0]["outcome"] = float("nan")
        with self.assertRaises(ValueError): observed_overlap(r, ["2025-10-01"])

if __name__ == "__main__": unittest.main()
