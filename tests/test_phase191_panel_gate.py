import hashlib,json,tempfile,unittest
from pathlib import Path
from scripts.phase191_panel_gate import audit
HEADER='security_id,exchange,trade_date,matched_group_id,outcome,contrast_pp\n'
ROW='AAA,XNAS,2025-10-01,G1,count,1.0\n'
class GateTests(unittest.TestCase):
    def check(self,rows=ROW,mutate=None,**changes):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'panel.csv';p.write_text(HEADER+rows)
            m={'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'source_url':'https://example.org/data','retrieved_utc':'2026-11-06T00:00:00Z','license_reviewed':True,'treatment_authenticated':True}
            m.update(changes)
            if mutate:mutate(p)
            q=Path(td)/'manifest.json';q.write_text(json.dumps(m))
            return audit(p,q)
    def test_valid(self):self.assertEqual(self.check()['rows'],1)
    def test_checksum(self):
        with self.assertRaisesRegex(ValueError,'checksum'):self.check(mutate=lambda p:p.write_text(HEADER+ROW+'x'))
    def test_duplicate(self):
        with self.assertRaisesRegex(ValueError,'duplicate'):self.check(rows=ROW+ROW)
    def test_weekend(self):
        with self.assertRaisesRegex(ValueError,'date'):self.check(rows=ROW.replace('2025-10-01','2025-10-04'))
    def test_authentication(self):
        with self.assertRaisesRegex(ValueError,'authentication'):self.check(treatment_authenticated=False)
    def test_nonfinite(self):
        with self.assertRaisesRegex(ValueError,'contrast'):self.check(rows=ROW.replace('1.0','nan'))
    def test_outcome(self):
        with self.assertRaisesRegex(ValueError,'outcome'):self.check(rows=ROW.replace('count','other'))
if __name__=='__main__':unittest.main()
