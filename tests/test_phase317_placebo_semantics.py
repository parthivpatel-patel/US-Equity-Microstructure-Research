import csv
import tempfile
import unittest
from pathlib import Path
from scripts.phase317_placebo_semantics import audit

FIELDS = ['outcome','nov_minus_oct_pp','pre_placebo_n','pre_placebo_at_least_as_negative','pre_placebo_at_least_as_extreme_absolute','pre_placebo_min_pp','pre_placebo_max_pp']
ROWS = [
 ['count','-0.7346606598677254','78','2','2','-1.4475738789418606','1.0538523294152946'],
 ['volume','0.626597999820323','78','48','76','-1.8665501312689659','1.4840122108986915']]

class TestAudit(unittest.TestCase):
    def check(self, rows, fields=FIELDS):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'x.csv'
            with p.open('w', newline='') as fh:
                w=csv.writer(fh);w.writerow(fields);w.writerows(rows)
            return audit(p)
    def test_frozen_summary(self):
        out=self.check(ROWS)
        self.assertEqual(out['count']['absolute_minus_negative_count'],0)
        self.assertEqual(out['volume']['absolute_minus_negative_count'],28)
        self.assertIsNone(out['volume']['calibrated_p_value'])
    def test_negative_impossibility(self):
        rows=[list(r) for r in ROWS];rows[0][4]='1'
        with self.assertRaises(ValueError):self.check(rows)
    def test_bad_counts(self):
        rows=[list(r) for r in ROWS];rows[0][3]='79'
        with self.assertRaises(ValueError):self.check(rows)
    def test_nonfinite(self):
        rows=[list(r) for r in ROWS];rows[0][1]='NaN'
        with self.assertRaises(ValueError):self.check(rows)
    def test_duplicate_outcome(self):
        with self.assertRaises(ValueError):self.check([ROWS[0],ROWS[0]])
    def test_duplicate_columns(self):
        with self.assertRaises(ValueError):self.check(ROWS,FIELDS+['outcome'])
    def test_outside_range(self):
        rows=[list(r) for r in ROWS];rows[0][1]='-3'
        with self.assertRaises(ValueError):self.check(rows)

if __name__=='__main__':unittest.main()
