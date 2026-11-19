"""Deterministic tests using only temporary constructed CSVs."""
import tempfile
import unittest
from pathlib import Path
from scripts.phase483_panel_integrity import audit

class IntegrityTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root = Path(self.tmp.name)
        self.cal = root / "calendar.csv"
        self.panel = root / "panel.csv"
        self.cal.write_text("date\n2025-10-01\n2025-10-02\n2025-10-03\n")
        self.panel.write_text("security,date,exchange,value\nA,2025-10-01,X,0\nA,2025-10-02,X,1\nA,2025-10-03,X,2\nB,2025-10-01,Y,5\n")

    def test_coverage_and_zero(self):
        x = audit(self.panel, self.cal, "2025-10-02")
        self.assertEqual(x["observed_zeros"], 1)
        self.assertEqual(x["missing_rows_against_observed_union"], 2)
        self.assertEqual(x["coverage_categories"]["complete_both"], 1)
        self.assertEqual(x["coverage_categories"]["complete_pre_only"], 1)

    def test_digest_changes(self):
        x = audit(self.panel, self.cal, "2025-10-02")["input_sha256"]["panel"]
        self.panel.write_text(self.panel.read_text().replace("Y,5", "Y,6"))
        self.assertNotEqual(x, audit(self.panel, self.cal, "2025-10-02")["input_sha256"]["panel"])

    def test_last_cutoff_rejected(self):
        with self.assertRaises(ValueError):
            audit(self.panel, self.cal, "2025-10-03")

    def test_duplicate_rejected(self):
        self.panel.write_text(self.panel.read_text() + "A,2025-10-01,X,0\n")
        with self.assertRaises(ValueError):
            audit(self.panel, self.cal, "2025-10-02")

    def test_nonfinite_rejected(self):
        self.panel.write_text(self.panel.read_text().replace("Y,5", "Y,nan"))
        with self.assertRaises(ValueError):
            audit(self.panel, self.cal, "2025-10-02")

    def test_off_calendar_rejected(self):
        self.panel.write_text(self.panel.read_text().replace("2025-10-01,Y", "2025-10-04,Y"))
        with self.assertRaises(ValueError):
            audit(self.panel, self.cal, "2025-10-02")

if __name__ == "__main__":
    unittest.main()
