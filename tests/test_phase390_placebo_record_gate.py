import csv
import tempfile
import unittest
from pathlib import Path
from phase390_placebo_record_gate import audit

H = 'a' * 64
BASE = dict(placebo_date='2025-10-15',estimate='0.2',estimand='trade_count',window_start='2025-10-01',window_end='2025-10-31',source_sha256=H)

class Tests(unittest.TestCase):
    def check(self, rows):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'p.csv'
            with p.open('w', newline='') as f:
                w = csv.DictWriter(f, fieldnames=BASE)
                w.writeheader()
                w.writerows(rows)
            return audit(p)
    def test_valid(self): self.assertEqual(self.check([BASE])['records'], 1)
    def test_empty(self):
        with self.assertRaises(ValueError): self.check([])
    def test_duplicate(self):
        with self.assertRaisesRegex(ValueError, 'duplicate'): self.check([BASE, BASE])
    def test_nonfinite(self):
        with self.assertRaisesRegex(ValueError, 'nonfinite'): self.check([{**BASE, 'estimate':'nan'}])
    def test_bad_hash(self):
        with self.assertRaisesRegex(ValueError, 'hash'): self.check([{**BASE, 'source_sha256':'x'}])
    def test_date_outside(self):
        with self.assertRaisesRegex(ValueError, 'outside'): self.check([{**BASE, 'placebo_date':'2025-09-01'}])
    def test_repeat_window(self):
        r = self.check([BASE, {**BASE, 'placebo_date':'2025-10-16'}])
        self.assertEqual(len(r['repeated_declared_windows']), 1)
    def test_different_estimands(self):
        self.assertEqual(self.check([BASE, {**BASE, 'estimand':'share_volume'}])['records'], 2)
    def test_invalid_date(self):
        with self.assertRaises(ValueError): self.check([{**BASE, 'placebo_date':'not-a-date'}])

if __name__ == '__main__':
    unittest.main()
