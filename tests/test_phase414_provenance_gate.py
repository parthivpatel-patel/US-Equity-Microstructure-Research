import hashlib
import tempfile
import unittest
from pathlib import Path
from scripts.phase414_provenance_gate import audit

class ProvenanceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "sample.csv").write_bytes(b"security,date\\nA,2025-10-01\\n")
        self.entry = {"path": "sample.csv", "sha256": hashlib.sha256((self.root / "sample.csv").read_bytes()).hexdigest(), "source_url": "https://example.org/source", "retrieved_utc": "2026-11-16T00:00:00Z", "redistribution": "restricted", "grain": "security-date"}
    def tearDown(self): self.tmp.cleanup()
    def check(self, entries): return audit({"sources": entries}, self.root)["status"]
    def test_valid_restricted_source_passes_integrity(self): self.assertEqual(self.check([self.entry]), "PASS")
    def test_tamper_blocks(self):
        (self.root / "sample.csv").write_bytes(b"changed")
        self.assertEqual(self.check([self.entry]), "BLOCKED")
    def test_missing_blocks(self):
        self.entry["path"] = "missing.csv"
        self.assertEqual(self.check([self.entry]), "BLOCKED")
    def test_traversal_blocks(self):
        self.entry["path"] = "../sample.csv"
        self.assertEqual(self.check([self.entry]), "BLOCKED")
    def test_duplicate_blocks(self): self.assertEqual(self.check([self.entry, self.entry]), "BLOCKED")
    def test_missing_rights_blocks(self):
        del self.entry["redistribution"]
        self.assertEqual(self.check([self.entry]), "BLOCKED")
    def test_empty_blocks(self): self.assertEqual(self.check([]), "BLOCKED")

if __name__ == "__main__": unittest.main()
