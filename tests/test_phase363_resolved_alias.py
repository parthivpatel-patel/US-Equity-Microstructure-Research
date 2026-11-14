import hashlib
import tempfile
import unittest
from pathlib import Path
from phase362_source_bytes import verify_source_bytes

class AliasTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / "sample.csv").write_bytes(b"fixture")
        self.digest = hashlib.sha256(b"fixture").hexdigest()

    def manifest(self, *paths):
        return [{"path": p, "sha256": self.digest} for p in paths]

    def test_dot_alias_rejected(self):
        with self.assertRaisesRegex(ValueError, "duplicate resolved"):
            verify_source_bytes(self.manifest("sample.csv", "./sample.csv"), self.root)

    def test_internal_symlink_alias_rejected(self):
        (self.root / "alias.csv").symlink_to(self.root / "sample.csv")
        with self.assertRaisesRegex(ValueError, "duplicate resolved"):
            verify_source_bytes(self.manifest("sample.csv", "alias.csv"), self.root)

    def test_single_file_valid(self):
        self.assertTrue(verify_source_bytes(self.manifest("sample.csv"), self.root)["all_bytes_match"])

    def test_distinct_identical_bytes_allowed(self):
        (self.root / "copy.csv").write_bytes(b"fixture")
        self.assertEqual(len(verify_source_bytes(self.manifest("sample.csv", "copy.csv"), self.root)["files"]), 2)

if __name__ == "__main__":
    unittest.main()
