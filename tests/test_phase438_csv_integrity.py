"""Constructed-data tests; no SEC observations."""
import csv
import hashlib
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from phase438_csv_integrity import audit_bytes
H=b'date,security,exchange,match_group,treated,hidden_count,total_count\n'
R=b'2025-10-30,A,X,G,1,2,10\n'
class CSVIntegrityTests(unittest.TestCase):
    def test_valid(self):
        a=audit_bytes(H+R)
        self.assertEqual(a['rows'],1)
        self.assertEqual(a['source_sha256'],hashlib.sha256(H+R).hexdigest())
        self.assertFalse(a['sec_source_authenticated'])
    def test_duplicate_header(self):
        with self.assertRaisesRegex(ValueError,'duplicate'):
            audit_bytes(H.replace(b'total_count',b'hidden_count')+R)
    def test_missing_column(self):
        with self.assertRaisesRegex(ValueError,'missing required'):
            audit_bytes(H.replace(b',total_count',b'')+R.replace(b',10',b''))
    def test_extra_field(self):
        with self.assertRaisesRegex(ValueError,'expected'):
            audit_bytes(H+R.rstrip(b'\n')+b',extra\n')
    def test_short_row(self):
        with self.assertRaisesRegex(ValueError,'expected'):
            audit_bytes(H+b'2025-10-30,A,X\n')
    def test_header_only(self):
        with self.assertRaisesRegex(ValueError,'header-only'):
            audit_bytes(H)
    def test_invalid_utf8(self):
        with self.assertRaisesRegex(ValueError,'UTF-8'):
            audit_bytes(H+b'\xff')
    def test_null(self):
        with self.assertRaisesRegex(ValueError,'NUL'):
            audit_bytes(H+R+b'\x00')
    def test_empty_field(self):
        with self.assertRaisesRegex(ValueError,'empty field'):
            audit_bytes(H+b'2025-10-30,,X,G,1,2,10\n')
    def test_quoted_comma(self):
        self.assertEqual(audit_bytes(H+b'2025-10-30,"A,B",X,G,1,2,10\n')['rows'],1)
    def test_unterminated_quote(self):
        with self.assertRaises(csv.Error):
            audit_bytes(H+b'2025-10-30,"A,X,G,1,2,10\n')
if __name__=='__main__':
    unittest.main()
