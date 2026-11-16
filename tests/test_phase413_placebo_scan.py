import unittest
from datetime import date,timedelta
from scripts.phase413_placebo_scan import scan
def rows(n=10):
    out=[];d=date(2025,10,1)
    while len({x['date'] for x in out})<n:
        if d.weekday()<5:
            for t in (0,1):out.append(dict(date=d.isoformat(),security=str(t),match_group='g',exchange='X',treated=str(t),hidden_trades=str(2+t),total_trades='10'))
        d+=timedelta(days=1)
    return out
class TestScan(unittest.TestCase):
    def test_zero(self):
        r=scan(rows(),('2025-10-08',),2);self.assertAlmostEqual(r['cutoffs'][0]['difference_pp'],0);self.assertAlmostEqual(r['cutoffs'][0]['hac_se_pp'],0)
    def test_duplicate(self):
        r=rows();self.assertEqual(scan(r+[r[0]])['status'],'BLOCKED')
    def test_invalid(self):
        r=rows();r[0]['hidden_trades']='11';self.assertEqual(scan(r)['status'],'BLOCKED')
    def test_no_overlap(self):self.assertEqual(scan([x for x in rows() if x['treated']=='1'])['status'],'BLOCKED')
    def test_insufficient(self):self.assertEqual(scan(rows(3),('2025-10-02',))['cutoffs'][0]['status'],'INSUFFICIENT_DATES')
    def test_cutoff(self):self.assertEqual(scan(rows(),('2025-11-03',))['status'],'BLOCKED')
    def test_change(self):
        r=rows()
        for x in r:
            if x['treated']=='1' and x['date']>='2025-10-08':x['hidden_trades']='8'
        self.assertGreater(scan(r,('2025-10-08',))['cutoffs'][0]['difference_pp'],0)
if __name__=='__main__':unittest.main()
