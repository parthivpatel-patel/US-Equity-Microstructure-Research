import hashlib, sys, tempfile, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from phase391_source_manifest_reconciliation import audit

class TestManifest(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name); self.raw=b'constructed fixture'
        self.h=hashlib.sha256(self.raw).hexdigest()
        (self.root/'source.csv').write_bytes(self.raw)
        self.rec=self.root/'records.csv'; self.man=self.root/'manifest.csv'
        self.record(self.h); self.manifest(self.h)
    def record(self,h):
        self.rec.write_text('placebo_date,estimand,source_sha256\n2025-10-01,count,'+h+'\n')
    def manifest(self,h,path='source.csv'):
        self.man.write_text('source_sha256,relative_path,redistribution_status\n'+h+','+path+',unknown\n')
    def test_manifest_only(self):
        self.assertFalse(audit(self.rec,self.man)['source_bytes_checked'])
    def test_matching_bytes_not_provenance(self):
        r=audit(self.rec,self.man,self.root)
        self.assertEqual(r['locally_checksum_verified_digests'],[self.h])
        self.assertFalse(r['source_origin_authenticated'])
        self.assertFalse(r['empirical_inference_ready'])
    def test_missing_manifest(self):
        self.record('a'*64)
        self.assertEqual(audit(self.rec,self.man)['missing_manifest_digests'],['a'*64])
    def test_changed_bytes(self):
        (self.root/'source.csv').write_bytes(b'changed')
        with self.assertRaisesRegex(ValueError,'checksum'): audit(self.rec,self.man,self.root)
    def test_duplicate_digest(self):
        with self.man.open('a') as f:f.write(self.h+',other.csv,unknown\n')
        with self.assertRaisesRegex(ValueError,'duplicate'):audit(self.rec,self.man)
    def test_traversal(self):
        self.manifest(self.h,'../outside.csv')
        with self.assertRaisesRegex(ValueError,'unsafe'):audit(self.rec,self.man)
    def test_absolute(self):
        self.manifest(self.h,'/tmp/x')
        with self.assertRaisesRegex(ValueError,'unsafe'):audit(self.rec,self.man)
    def test_bad_hash(self):
        self.record('bad')
        with self.assertRaisesRegex(ValueError,'SHA-256'):audit(self.rec,self.man)
    def test_missing_local(self):
        (self.root/'source.csv').unlink()
        self.assertEqual(audit(self.rec,self.man,self.root)['missing_local_source_digests'],[self.h])
    def test_duplicate_headers(self):
        self.rec.write_text('source_sha256,source_sha256,placebo_date,estimand\n')
        with self.assertRaisesRegex(ValueError,'headers'):audit(self.rec,self.man)
    def test_symlink_escape(self):
        outside=self.root.parent/('phase391-'+self.root.name)
        outside.write_bytes(self.raw);self.addCleanup(lambda:outside.unlink(missing_ok=True))
        (self.root/'source.csv').unlink();(self.root/'source.csv').symlink_to(outside)
        with self.assertRaisesRegex(ValueError,'escapes'):audit(self.rec,self.man,self.root)
if __name__=='__main__':unittest.main()
