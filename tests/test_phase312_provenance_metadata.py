import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from scripts.phase312_provenance_metadata import verify_manifest_strict

class MetadataTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        (self.root/'data.csv').write_bytes(b'abc')
        self.item={'path':'data.csv','sha256':hashlib.sha256(b'abc').hexdigest(),'source_url':'https://www.sec.gov/files/data.csv','retrieved_utc':'2026-11-11T12:00:00Z'}
    def check(self, entries):
        m=self.root/'manifest.json';m.write_text(json.dumps({'sources':entries}))
        return verify_manifest_strict(m,self.root)
    def test_valid(self): self.assertEqual(len(self.check([self.item])),1)
    def test_invalid_february(self):
        with self.assertRaisesRegex(ValueError,'calendar timestamp'): self.check([dict(self.item,retrieved_utc='2026-02-30T12:00:00Z')])
    def test_invalid_hour(self):
        with self.assertRaisesRegex(ValueError,'calendar timestamp'): self.check([dict(self.item,retrieved_utc='2026-11-11T25:00:00Z')])
    def test_url_missing_host(self):
        with self.assertRaisesRegex(ValueError,'source URL'): self.check([dict(self.item,source_url='https://')])
    def test_url_userinfo(self):
        with self.assertRaisesRegex(ValueError,'source URL'): self.check([dict(self.item,source_url='https://user:pass@sec.gov/a')])
    def test_canonical_alias(self):
        (self.root/'alias.csv').symlink_to(self.root/'data.csv')
        with self.assertRaisesRegex(ValueError,'duplicate canonical'): self.check([self.item,dict(self.item,path='alias.csv')])
    def test_hash_tamper(self):
        with self.assertRaisesRegex(ValueError,'checksum mismatch'): self.check([dict(self.item,sha256='0'*64)])
if __name__=='__main__': unittest.main()
