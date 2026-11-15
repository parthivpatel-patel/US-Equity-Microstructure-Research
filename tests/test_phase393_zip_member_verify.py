import hashlib, sys, tempfile, unittest, warnings, zipfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from phase393_zip_member_verify import verify

class ZipVerificationTests(unittest.TestCase):
    def make(self, members):
        tmp = tempfile.TemporaryDirectory()
        p = Path(tmp.name) / "test.zip"
        with zipfile.ZipFile(p, "w", compression=zipfile.ZIP_DEFLATED) as z:
            for name, content in members:
                z.writestr(name, content)
        self.addCleanup(tmp.cleanup)
        return p

    def test_bytes_hash(self):
        r = verify(self.make([("a.txt", b"abc")]))
        self.assertEqual(r["status"], "verified_bytes_only")
        self.assertEqual(r["members"][0]["sha256"], hashlib.sha256(b"abc").hexdigest())
        self.assertFalse(r["source_authenticated"])
    def test_traversal(self):
        self.assertEqual(verify(self.make([("../escape", b"x")]))["status"], "rejected")
    def test_absolute(self):
        self.assertEqual(verify(self.make([("/root", b"x")]))["status"], "rejected")
    def test_duplicate(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            p = self.make([("same", b"a"), ("same", b"b")])
        self.assertEqual(verify(p)["reason"], "unsafe_member")
    def test_total_limit(self):
        self.assertEqual(verify(self.make([("a", b"ab"), ("b", b"cd")]),
                                max_total_bytes=3)["status"], "rejected")
    def test_member_limit(self):
        self.assertEqual(verify(self.make([("a", b"ab")]),
                                max_member_bytes=1)["status"], "rejected")
    def test_member_count(self):
        self.assertEqual(verify(self.make([("a", b"1"), ("b", b"2")]),
                                max_members=1)["reason"], "member_count_limit")
    def test_empty(self):
        self.assertEqual(verify(self.make([]))["bytes_verified"], 0)
    def test_invalid_limits(self):
        with self.assertRaises(ValueError):
            verify(self.make([]), chunk_size=0)
    def test_crc_corruption(self):
        p = self.make([("abc", b"hello world")])
        with zipfile.ZipFile(p, "w", compression=zipfile.ZIP_STORED) as z:
            z.writestr("abc", b"hello world")
        data = bytearray(p.read_bytes())
        data[data.index(b"hello world")] ^= 1
        p.write_bytes(data)
        self.assertEqual(verify(p)["reason"], "member_read_or_crc_error")

if __name__ == "__main__":
    unittest.main()
