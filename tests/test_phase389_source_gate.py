import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from scripts.phase389_source_gate import audit

class SourceGateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root/'sample.txt').write_bytes(b'fixture')
        self.row = {'path':'sample.txt','sha256':hashlib.sha256(b'fixture').hexdigest(), 'bytes':7,
                    'origin_url':'https://example.org/data','retrieved_utc':'2026-11-15T00:00:00Z',
                    'license_status':'unknown','role':'test fixture'}
    def run_rows(self, rows):
        f=self.root/'manifest.json';f.write_text(json.dumps(rows));return audit(self.root,f)
    def test_integrity_not_permission(self):
        r=self.run_rows([self.row]);self.assertEqual(r['verified'],1);self.assertEqual(r['eligible_for_review'],0)
    def test_manifest_permission_not_independent(self):
        self.row['license_status']='redistributable';r=self.run_rows([self.row]);self.assertEqual(r['eligible_for_review'],1);self.assertFalse(r['redistribution_permission_independently_verified'])
    def test_changed_file(self):
        (self.root/'sample.txt').write_bytes(b'changed');self.assertFalse(self.run_rows([self.row])['records'][0]['integrity_verified'])
    def test_missing_file(self):
        self.row['path']='missing.txt';self.assertFalse(self.run_rows([self.row])['records'][0]['exists'])
    def test_duplicate(self):
        with self.assertRaises(ValueError):self.run_rows([self.row,self.row])
    def test_traversal(self):
        self.row['path']='../outside'
        with self.assertRaises(ValueError):self.run_rows([self.row])
    def test_bad_digest(self):
        self.row['sha256']='0'
        with self.assertRaises(ValueError):self.run_rows([self.row])
    def test_bad_license(self):
        self.row['license_status']='public domain'
        with self.assertRaises(ValueError):self.run_rows([self.row])
    def test_missing_metadata(self):
        self.row['origin_url']='';self.assertFalse(self.run_rows([self.row])['records'][0]['metadata_complete'])
    def test_empty_inventory(self):
        self.assertEqual(self.run_rows([])['entries'],0)

if __name__=='__main__':unittest.main()
