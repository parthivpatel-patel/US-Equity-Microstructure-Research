import hashlib
from pathlib import Path
import tempfile
import unittest
from scripts.phase417_provenance_gate import audit

class GateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "a.csv").write_bytes(b"example fixture")
        self.entry = {"path":"a.csv", "sha256":hashlib.sha256(b"example fixture").hexdigest(), "source_url":"https://www.sec.gov/test", "retrieved_utc":"2026-11-16T20:00:00Z", "redistribution":"restricted", "grain":"security-date-exchange"}
    def tearDown(self):
        self.tmp.cleanup()
    def check(self, entries):
        return audit({"sources":entries}, self.root)
    def test_valid_restricted_not_publication_clearance(self):
        r = self.check([self.entry])
        self.assertEqual(r["status"], "PASS")
        self.assertEqual(r["publication_clearance"], "NOT_ESTABLISHED")
    def test_canonical_alias(self):
        self.assertEqual(self.check([self.entry, dict(self.entry, path="./a.csv")])["status"], "BLOCKED")
    def test_invalid_timestamp(self):
        self.assertEqual(self.check([dict(self.entry, retrieved_utc="yesterday")])["status"], "BLOCKED")
    def test_naive_timestamp(self):
        self.assertEqual(self.check([dict(self.entry, retrieved_utc="2026-11-16T20:00:00")])["status"], "BLOCKED")
    def test_non_utc_timestamp(self):
        self.assertEqual(self.check([dict(self.entry, retrieved_utc="2026-11-16T20:00:00-05:00")])["status"], "BLOCKED")
    def test_http_url(self):
        self.assertEqual(self.check([dict(self.entry, source_url="http://example.com")])["status"], "BLOCKED")
    def test_unsupported_grain(self):
        self.assertEqual(self.check([dict(self.entry, grain="unknown")])["status"], "BLOCKED")
    def test_hash_mismatch(self):
        self.assertEqual(self.check([dict(self.entry, sha256="0"*64)])["status"], "BLOCKED")
    def test_traversal(self):
        self.assertEqual(self.check([dict(self.entry, path="../a.csv")])["status"], "BLOCKED")
    def test_empty(self):
        self.assertEqual(self.check([])["status"], "BLOCKED")
    def test_unknown_rights_not_clearance(self):
        self.assertEqual(self.check([dict(self.entry, redistribution="unknown")])["publication_clearance"], "NOT_ESTABLISHED")
    def test_invalid_rights(self):
        self.assertEqual(self.check([dict(self.entry, redistribution="open")])["status"], "BLOCKED")
    def test_missing_file(self):
        self.assertEqual(self.check([dict(self.entry, path="missing.csv")])["status"], "BLOCKED")

if __name__ == "__main__":
    unittest.main()
