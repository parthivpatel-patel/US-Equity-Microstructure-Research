import hashlib
import os
import tempfile
import unittest
from pathlib import Path
from phase362_source_bytes import verify_source_bytes

class HardlinkAliasTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / "sample.csv").write_bytes(b"fixture")
        self.digest = hashlib.sha256(b"fixture").hexdigest()

    def manifest(self, *paths):
        return [{"path": p, "sha256": self.digest} for p in paths]

    def test_hardlink_alias_rejected(self):
        os.link(self.root / "sample.csv", self.root / "hardlink.csv")
        with self.assertRaisesRegex(ValueError, "duplicate underlying"):
            verify_source_bytes(self.manifest("sample.csv", "hardlink.csv"), self.root)

    def test_distinct_identical_files_allowed(self):
        (self.root / "copy.csv").write_bytes(b"fixture")
        self.assertTrue(verify_source_bytes(self.manifest("sample.csv", "copy.csv"), self.root)["all_bytes_match"])

    def test_single_file_accepted(self):
        self.assertEqual(verify_source_bytes(self.manifest("sample.csv"), self.root)["files"][0]["size_bytes"], 7)

    def test_mismatched_digest_reported(self):
        (self.root / "sample.csv").write_bytes(b"changed")
        self.assertFalse(verify_source_bytes(self.manifest("sample.csv"), self.root)["all_bytes_match"])

if __name__ == "__main__":
    unittest.main()
