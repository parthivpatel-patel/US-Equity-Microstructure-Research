import unittest
from scripts.phase455_support_attrition import audit

def r(s,e,g,d,t,y=1.):
    return dict(security=s,exchange=e,matched_group=g,date=d,treated=t,outcome=y)

class Tests(unittest.TestCase):
    def test_full_support(self):
        rows=[r('T','X','A',d,True) for d in ('2025-10-31','2025-11-03')]+[r('C','X','A',d,False) for d in ('2025-10-31','2025-11-03')]
        a=audit(rows)
        self.assertEqual(a['fully_balanced_calendar_dates'],2)
        self.assertEqual(a['periods']['pre']['retained_fraction'],1)
        self.assertEqual(a['periods']['post']['retained_fraction'],1)
    def test_global_balancing_discards_locally_paired(self):
        rows=[r(s,'X',g,d,t) for g in ('A','B') for d in ('2025-10-31','2025-11-03') for s,t in ((g+'T',True),(g+'C',False)) if not (g=='B' and d=='2025-11-03' and t==False)]
        a=audit(rows)
        self.assertEqual(a['periods']['post']['paired_stratum_date_cells'],1)
        self.assertEqual(a['periods']['post']['globally_retained_stratum_date_cells'],0)
        self.assertEqual(a['periods']['post']['retained_fraction'],0)
    def test_duplicate(self):
        row=r('T','X','A','2025-10-31',True)
        with self.assertRaisesRegex(ValueError,'duplicate'): audit([row,row])
    def test_unstable_assignment(self):
        with self.assertRaisesRegex(ValueError,'unstable'): audit([r('T','X','A','2025-10-31',True),r('T','X','B','2025-11-03',True)])
    def test_nonfinite(self):
        with self.assertRaisesRegex(ValueError,'outcome'): audit([r('T','X','A','2025-10-31',True,float('nan'))])
    def test_empty(self):
        with self.assertRaisesRegex(ValueError,'empty'): audit([])
    def test_no_pre(self):
        a=audit([r('T','X','A','2025-11-03',True)])
        self.assertIsNone(a['periods']['pre']['retained_fraction'])
    def test_treatment_type(self):
        with self.assertRaisesRegex(ValueError,'treatment'): audit([r('T','X','A','2025-10-31',1)])

if __name__=='__main__': unittest.main()
