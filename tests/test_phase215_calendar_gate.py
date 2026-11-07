import unittest
from scripts.phase215_calendar_gate import admit_sessions

D=['2025-10-01','2025-10-02','2025-10-03','2025-10-06','2025-10-07','2025-10-08']
R=[{'date':d,'contrast':float(i)} for i,d in enumerate(D)]
E=(D[0],D[1]); L=(D[4],D[5])
class GateTests(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(admit_sessions(R,D,E,L)['gap_sessions'],2)
    def test_missing_session(self):
        with self.assertRaises(ValueError): admit_sessions(R[:-1],D,E,L)
    def test_duplicate_calendar(self):
        with self.assertRaises(ValueError): admit_sessions(R,D+[D[-1]],E,L)
    def test_duplicate_rows(self):
        with self.assertRaises(ValueError): admit_sessions(R+[R[-1]],D,E,L)
    def test_unsorted_rows(self):
        with self.assertRaises(ValueError): admit_sessions(R[::-1],D,E,L)
    def test_invalid_value(self):
        with self.assertRaises(ValueError): admit_sessions(R[:-1]+[{'date':D[-1],'contrast':float('nan')}],D,E,L)
    def test_reform_intrusion(self):
        with self.assertRaises(ValueError): admit_sessions(R+[{'date':'2025-11-03','contrast':1}],D+['2025-11-03'],E,L)
    def test_bad_endpoint(self):
        with self.assertRaises(ValueError): admit_sessions(R,D,('2025-10-04',D[1]),L)
    def test_overlap(self):
        with self.assertRaises(ValueError): admit_sessions(R,D,E,(D[1],D[5]))
    def test_noncanonical_date(self):
        with self.assertRaises(ValueError): admit_sessions(R,['2025-10-1']+D[1:],E,L)
    def test_weekend_gap_not_counted(self):
        self.assertEqual(admit_sessions(R,D,E,L)['gap_sessions'],2)
if __name__=='__main__': unittest.main()
