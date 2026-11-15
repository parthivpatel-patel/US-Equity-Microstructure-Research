import csv
import tempfile
import unittest
from pathlib import Path
from scripts.phase371_panel_gate import REQUIRED, audit

class PanelGateTests(unittest.TestCase):
    def check(self, rows):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'fixture.csv'
            with path.open('w', newline='') as fh:
                writer = csv.writer(fh)
                writer.writerow(REQUIRED)
                writer.writerows(rows)
            return audit(path)

    def test_valid_panel(self):
        result = self.check([('A','2025-10-31','XNAS','treated',1,2,5,10),('B','2025-10-31','XNYS','control',0,2,0,10)])
        self.assertTrue(result['passed'])
        self.assertEqual((result['treated_securities'], result['control_securities']), (1,1))
        self.assertFalse(result['source_authenticated'])

    def test_duplicate(self):
        row = ('A','2025-10-31','XNAS','treated',1,2,5,10)
        self.assertEqual(self.check([row,row])['issues']['duplicate_security_date_exchange'],1)

    def test_cohort_switch(self):
        a = ('A','2025-10-30','XNAS','treated',1,2,5,10)
        b = ('A','2025-10-31','XNAS','control',1,2,5,10)
        self.assertEqual(self.check([a,b])['issues']['cohort_switch'],1)

    def test_bad_measure(self):
        r = self.check([('A','2025-10-31','XNAS','treated','nan',2,5,10)])
        self.assertIn('invalid_measure',r['issues'])

    def test_impossible_ratio(self):
        r = self.check([('A','2025-10-31','XNAS','treated',3,2,11,10)])
        self.assertIn('numerator_exceeds_denominator',r['issues'])

    def test_noncanonical_date(self):
        r = self.check([('A','2025-1-3','XNAS','treated',1,2,5,10)])
        self.assertIn('invalid_date',r['issues'])

    def test_empty(self):
        self.assertFalse(self.check([])['passed'])

    def test_fractional_count(self):
        self.assertIn('invalid_measure', self.check([('A','2025-10-31','XNAS','treated',0.5,2,5,10)])['issues'])

if __name__ == '__main__':
    unittest.main()
