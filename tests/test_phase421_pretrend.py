import unittest
from phase421_pretrend import analyze

def rows():
    out=[]
    for i,d in enumerate(['2025-09-02','2025-09-03','2025-09-04']):
        out += [dict(date=d,security='A',exchange='X',match_group='G',treated='1',hidden_count=str(1+i),total_count='10'),dict(date=d,security='B',exchange='X',match_group='G',treated='0',hidden_count='1',total_count='10')]
    return out

class Tests(unittest.TestCase):
    def test_slope(self): self.assertAlmostEqual(analyze(rows())['september_slope_per_calendar_day'],.1)
    def test_duplicate(self):
        with self.assertRaisesRegex(ValueError,'duplicate'):analyze(rows()+[rows()[0]])
    def test_invalid_count(self):
        r=rows();r[0]['hidden_count']='11'
        with self.assertRaisesRegex(ValueError,'counts'):analyze(r)
    def test_missing_arm(self):
        with self.assertRaisesRegex(ValueError,'three'):analyze([r for r in rows() if r['treated']=='1'])
    def test_post_date(self):
        r=rows();r[0]['date']='2025-11-03'
        with self.assertRaisesRegex(ValueError,'outside'):analyze(r)
    def test_missing_column(self):
        r=rows();del r[0]['exchange']
        with self.assertRaisesRegex(ValueError,'columns'):analyze(r)

if __name__=='__main__':unittest.main()
