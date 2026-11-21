import csv,importlib.util,tempfile,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/'scripts'/'historical_roster_audit.py';spec=importlib.util.spec_from_file_location('roster',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Test(unittest.TestCase):
 def setUp(self):
  self.t=tempfile.TemporaryDirectory();d=Path(self.t.name);self.n=d/'nyse.csv';self.q=d/'nasdaq.csv';self.p=d/'panel.csv'
  self.write(self.n,['Measurement Month','Trade Date','Symbol','Refsym','Listed Mic','Round Lot Size'],[['202509','20251031','ABC','1','XNYS','40']])
  self.write(self.q,['evaluation_period','issue_id','ticker','average_closing_price','round_lot'],[['202609','2','XYZ','10','100'],['2026-10-01 02:35:26','','','','']])
  self.write(self.p,['Ticker','treated'],[['XYZ','1'],['DEF','0']])
 def tearDown(self):self.t.cleanup()
 def write(self,p,head,rows):
  with p.open('w',newline='') as f:w=csv.writer(f);w.writerow(head);w.writerows(rows)
 def test_counts(self):
  x=m.audit(self.n,self.q,self.p);self.assertEqual(x['nyse_snapshot']['rows'],1);self.assertEqual(x['nasdaq_file']['invalid_or_non_data_rows'],1)
 def test_no_overlap(self):self.assertEqual(m.audit(self.n,self.q,self.p)['overlap']['panel_tickers_in_nyse_listing_snapshot'],0)
 def test_hash(self):self.assertEqual(len(m.audit(self.n,self.q,self.p)['inputs']['nyse_file_sha256']),64)
 def test_wrong_month(self):
  self.write(self.n,['Measurement Month','Trade Date','Symbol','Refsym','Listed Mic','Round Lot Size'],[['202508','20251031','ABC','1','XNYS','40']]);self.assertRaises(ValueError,m.audit,self.n,self.q,self.p)
 def test_duplicate(self):
  self.write(self.n,['Measurement Month','Trade Date','Symbol','Refsym','Listed Mic','Round Lot Size'],[['202509','20251031','ABC','1','XNYS','40'],['202509','20251031','ABC','2','XNYS','40']]);self.assertRaises(ValueError,m.audit,self.n,self.q,self.p)
 def test_invalid_lot(self):
  self.write(self.n,['Measurement Month','Trade Date','Symbol','Refsym','Listed Mic','Round Lot Size'],[['202509','20251031','ABC','1','XNYS','3']]);self.assertRaises(ValueError,m.audit,self.n,self.q,self.p)
 def test_overlap(self):
  self.write(self.p,['Ticker','treated'],[['ABC','1'],['DEF','0']]);self.assertEqual(m.audit(self.n,self.q,self.p)['overlap']['treated_panel_tickers_in_nyse_listing_snapshot'],1)
 def test_bad_label(self):
  self.write(self.p,['Ticker','treated'],[['XYZ','2']]);self.assertRaises(ValueError,m.audit,self.n,self.q,self.p)
if __name__=='__main__':unittest.main()
