import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from scripts.phase311_source_gate import verify_sources


class SourceGateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / 'panel.csv').write_bytes(b'security,date\nABC,2025-11-03\n')
        self.entry = dict(path='panel.csv', sha256=hashlib.sha256((self.root / 'panel.csv').read_bytes()).hexdigest(), source_url='https://www.sec.gov/example', retrieved_utc='2026-11-11T12:00:00Z')

    def check(self, sources):
        p = self.root / 'manifest.json'
        p.write_text(json.dumps({'sources': sources}))
        return verify_sources(p, self.root)

    def test_valid(self):
        self.assertEqual(len(self.check([self.entry])), 1)

    def test_tampered(self):
        (self.root / 'panel.csv').write_bytes(b'changed')
        with self.assertRaisesRegex(ValueError, 'checksum mismatch'): self.check([self.entry])

    def test_empty(self):
        with self.assertRaises(ValueError): self.check([])

    def test_duplicate(self):
        with self.assertRaises(ValueError): self.check([self.entry, self.entry])

    def test_traversal(self):
        with self.assertRaises(ValueError): self.check([dict(self.entry, path='../outside')])

    def test_bad_digest(self):
        with self.assertRaises(ValueError): self.check([dict(self.entry, sha256='123')])

    def test_missing_provenance(self):
        with self.assertRaises(ValueError): self.check([dict(self.entry, source_url='')])

    def test_missing_file(self):
        with self.assertRaises(FileNotFoundError): self.check([dict(self.entry, path='missing.csv')])

    def test_symlink_escape(self):
        outside = self.root.parent / ('outside-' + self.root.name)
        outside.write_bytes(b'outside')
        self.addCleanup(lambda: outside.unlink(missing_ok=True))
        (self.root / 'escape.csv').symlink_to(outside)
        with self.assertRaises(ValueError): self.check([dict(self.entry, path='escape.csv')])

if __name__ == '__main__': unittest.main()
