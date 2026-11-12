import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from scripts.phase313_url_authority import verify_authorities

class URLAuthorityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'sample.csv').write_bytes(b'abc')
        self.entry = {'path':'sample.csv', 'sha256':hashlib.sha256(b'abc').hexdigest(), 'source_url':'https://www.sec.gov/sample.csv', 'retrieved_utc':'2026-11-11T12:00:00Z'}
    def check(self, url):
        item = dict(self.entry, source_url=url)
        manifest = self.root / 'manifest.json'
        manifest.write_text(json.dumps({'sources':[item]}), encoding='utf-8')
        return verify_authorities(manifest, self.root)
    def test_valid(self):
        self.assertEqual(len(self.check('https://www.sec.gov/sample.csv')), 1)
    def test_explicit_default_port(self):
        self.assertEqual(len(self.check('https://www.sec.gov:443/sample.csv')), 1)
    def test_invalid_port(self):
        with self.assertRaisesRegex(ValueError, 'authority'): self.check('https://www.sec.gov:abc/sample.csv')
    def test_out_of_range_port(self):
        with self.assertRaisesRegex(ValueError, 'authority'): self.check('https://www.sec.gov:65536/sample.csv')
    def test_nonstandard_port(self):
        with self.assertRaisesRegex(ValueError, 'nonstandard'): self.check('https://www.sec.gov:8443/sample.csv')
    def test_backslash(self):
        with self.assertRaisesRegex(ValueError, 'unsafe'): self.check('https://www.sec.gov\\@evil.example/sample.csv')
    def test_single_label(self):
        with self.assertRaisesRegex(ValueError, 'host labels'): self.check('https://localhost/sample.csv')
    def test_ip_literal(self):
        with self.assertRaisesRegex(ValueError, 'IP literal'): self.check('https://127.0.0.1/sample.csv')
    def test_bad_dns_label(self):
        with self.assertRaisesRegex(ValueError, 'host labels'): self.check('https://-invalid.example/sample.csv')
    def test_userinfo(self):
        with self.assertRaisesRegex(ValueError, 'authority'): self.check('https://user@www.sec.gov/sample.csv')
if __name__ == '__main__': unittest.main()
