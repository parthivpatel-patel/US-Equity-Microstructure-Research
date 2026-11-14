import hashlib
import tempfile
import unittest
from pathlib import Path
from phase362_source_bytes import verify_source_bytes

class SourceByteTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "sample.csv").write_bytes(b"a,b\n1,2\n")
        self.good = hashlib.sha256(b"a,b\n1,2\n").hexdigest()
    def test_match(self):
        r = verify_source_bytes([{"path":"sample.csv","sha256":self.good}], self.root)
        self.assertTrue(r["all_bytes_match"])
        self.assertFalse(r["historical_source_authenticated"])
    def test_mismatch(self):
        self.assertFalse(verify_source_bytes([{"path":"sample.csv","sha256":"0"*64}], self.root)["all_bytes_match"])
    def test_traversal(self):
        with self.assertRaises(ValueError): verify_source_bytes([{"path":"../other","sha256":self.good}], self.root)
    def test_duplicate(self):
        with self.assertRaises(ValueError): verify_source_bytes([{"path":"sample.csv","sha256":self.good}]*2, self.root)
    def test_invalid_digest(self):
        with self.assertRaises(ValueError): verify_source_bytes([{"path":"sample.csv","sha256":"x"*64}], self.root)
    def test_empty(self):
        with self.assertRaises(ValueError): verify_source_bytes([], self.root)
    def test_symlink_escape(self):
        outside = self.root.parent / "outside_phase362_fixture"
        outside.write_bytes(b"not research data")
        self.addCleanup(lambda: outside.unlink(missing_ok=True))
        (self.root/"link").symlink_to(outside)
        with self.assertRaises(ValueError): verify_source_bytes([{"path":"link","sha256":self.good}], self.root)

if __name__ == "__main__": unittest.main()
