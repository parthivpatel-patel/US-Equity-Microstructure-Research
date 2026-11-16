import csv
import tempfile
import unittest
from pathlib import Path
from phase405_date_coverage import audit

FIELDS=['Date','lot','Hidden','TradesForHidden',"HiddenVol('000)","TradeVolForHidden('000)"]
class CoverageTests(unittest.TestCase):
    def run_rows(self, rows):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'input.csv'
            with p.open('w',newline='') as f:
                w=csv.DictWriter(f,fieldnames=FIELDS);w.writeheader();w.writerows(rows)
            return audit(p)
    def sample(self, date='20251001'):
        return [dict(zip(FIELDS,[date,lot,1,2,3,4])) for lot in (10,40,100)]
    def test_complete(self):
        x=self.run_rows(self.sample());self.assertTrue(x['complete']);self.assertEqual(x['distinct_dates'],1)
    def test_missing(self):
        x=self.run_rows(self.sample()[:2]);self.assertEqual(x['missing_tiers_by_date']['2025-10-01'],[100])
    def test_duplicate(self):
        x=self.run_rows(self.sample()+self.sample()[:1]);self.assertEqual(x['duplicate_rows'],[5])
    def test_weekend(self):
        x=self.run_rows(self.sample('20251004'));self.assertFalse(x['complete']);self.assertEqual(len(x['invalid_rows']),3)
    def test_bad_rate(self):
        r=self.sample();r[0]['Hidden']=3;self.assertFalse(self.run_rows(r)['complete'])
    def test_iso_date(self):
        self.assertTrue(self.run_rows(self.sample('2025-10-01'))['complete'])
    def test_empty(self):
        with self.assertRaises(ValueError):self.run_rows([])
if __name__=='__main__':unittest.main()
