import hashlib
import tempfile
import unittest
from pathlib import Path
from scripts.phase266_source_manifest import inspect

class ManifestTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / "sample.csv").write_bytes(b"a,b\n1,2\n")
        self.rec = {"path": "sample.csv", "sha256": hashlib.sha256(b"a,b\n1,2\n").hexdigest(), "size_bytes": 8}
    def test_valid(self):
        r = inspect(self.root, [self.rec])
        self.assertTrue(r["byte_integrity_pass"])
        self.assertFalse(r["historical_inference_authorized"])
        self.assertFalse(r["source_authentication_pass"])
    def test_missing(self):
        self.assertEqual(inspect(self.root, [{**self.rec, "path": "missing"}])["files"][0]["status"], "missing")
    def test_tamper(self):
        (self.root / "sample.csv").write_bytes(b"a,b\n9,2\n")
        self.assertEqual(inspect(self.root, [self.rec])["files"][0]["status"], "mismatch")
    def test_empty(self):
        self.assertFalse(inspect(self.root, [])["byte_integrity_pass"])
    def test_duplicate(self):
        with self.assertRaises(ValueError): inspect(self.root, [self.rec, self.rec])
    def test_traversal(self):
        with self.assertRaises(ValueError): inspect(self.root, [{**self.rec, "path": "../outside"}])
    def test_absolute(self):
        with self.assertRaises(ValueError): inspect(self.root, [{**self.rec, "path": "/etc/passwd"}])
    def test_bad_sha(self):
        with self.assertRaises(ValueError): inspect(self.root, [{**self.rec, "sha256": "0" * 63}])
    def test_boolean_size(self):
        with self.assertRaises(ValueError): inspect(self.root, [{**self.rec, "size_bytes": True}])
    def test_symlink_escape(self):
        (self.root / "escape").symlink_to("/etc/passwd")
        with self.assertRaises(ValueError): inspect(self.root, [{**self.rec, "path": "escape"}])

if __name__ == "__main__":
    unittest.main()
