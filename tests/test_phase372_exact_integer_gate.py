import csv
import tempfile
import unittest
from pathlib import Path
from scripts.phase372_exact_integer_gate import audit, exact_nonnegative_integer

class ExactIntegerGateTests(unittest.TestCase):
    def test_large_integer_exact(self):
        self.assertEqual(exact_nonnegative_integer('9007199254740993'), 9007199254740993)
    def test_fraction_rejected(self):
        with self.assertRaises(ValueError): exact_nonnegative_integer('2.5')
    def test_nonfinite_rejected(self):
        for v in ('NaN', 'Infinity', '-1'):
            with self.subTest(v=v), self.assertRaises(ValueError): exact_nonnegative_integer(v)
    def test_precision_sensitive_inequality(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)/'data.csv'
            with p.open('w', newline='') as f:
                w=csv.writer(f)
                w.writerow(['hidden_count','total_count','hidden_volume','total_volume'])
                w.writerow(['9007199254740993','9007199254740992','0','0'])
            r=audit(p)
            self.assertFalse(r['passed'])
            self.assertEqual(r['errors'][0]['issue'],'numerator_exceeds_denominator')
    def test_valid_large_integer(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'data.csv'
            p.write_text('hidden_count,total_count,hidden_volume,total_volume\n9007199254740992,9007199254740993,0,0\n')
            self.assertTrue(audit(p)['passed'])
    def test_extra_field_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'data.csv'
            p.write_text('hidden_count,total_count,hidden_volume,total_volume\n1,2,3,4,5\n')
            self.assertEqual(audit(p)['errors'][0]['issue'],'malformed_row')

if __name__ == '__main__': unittest.main()
