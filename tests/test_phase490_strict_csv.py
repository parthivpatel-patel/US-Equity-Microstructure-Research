"""Regression tests for strict CSV admission; synthetic fixtures only."""
import tempfile
import unittest
from pathlib import Path
from scripts.phase490_strict_csv import read_strict

class StrictCSVTests(unittest.TestCase):
    def check(self, body, observed=False, error=None):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'input.csv'
            path.write_text(body, encoding='utf-8')
            if error:
                with self.assertRaisesRegex(ValueError, error):
                    read_strict(path, observed)
            else:
                return read_strict(path, observed)

    def test_zero_is_observed(self):
        data = self.check('security,exchange,date,outcome\nA,X,2025-10-01,0\n', True)
        self.assertEqual(next(iter(data.values())), 0)

    def test_extra_column_in_row(self):
        self.check('security,exchange,date,outcome\nA,X,2025-10-01,0,EXTRA\n', True, 'malformed CSV row')

    def test_missing_column_in_row(self):
        self.check('security,exchange,date,outcome\nA,X,2025-10-01\n', True, 'malformed CSV row')

    def test_duplicate_header(self):
        self.check('security,exchange,date,date\nA,X,2025-10-01,2025-10-01\n', False, 'invalid CSV schema')

    def test_duplicate_key(self):
        self.check('security,exchange,date\nA,X,2025-10-01\nA,X,2025-10-01\n', False, 'duplicate key')

    def test_nonfinite(self):
        self.check('security,exchange,date,outcome\nA,X,2025-10-01,nan\n', True, 'nonfinite')

    def test_invalid_date(self):
        self.check('security,exchange,date\nA,X,2025-02-30\n', False, 'invalid date')

    def test_valid_eligibility(self):
        self.assertEqual(len(self.check('security,exchange,date\nA,X,2025-10-01\nB,Y,2025-10-02\n')), 2)

if __name__ == '__main__':
    unittest.main()
