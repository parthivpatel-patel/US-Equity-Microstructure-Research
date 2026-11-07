"""Independent sandwich reference for Phase 213; synthetic data only."""
import unittest
from datetime import date, timedelta
from math import sqrt
from scripts.phase213_joint_hac import joint_window_hac


def reference(rows, early, late, lag):
    dates = [r['date'] for r in rows]
    e = [i for i, d in enumerate(dates) if early[0] <= d <= early[1]]
    l = [i for i, d in enumerate(dates) if late[0] <= d <= late[1]]
    ye = sum(rows[i]['contrast'] for i in e) / len(e)
    yl = sum(rows[i]['contrast'] for i in l) / len(l)
    # OLS sandwich for two disjoint window indicators, including zero-score gaps.
    x = [(int(i in e), int(i in l)) for i in range(len(rows))]
    residual = [rows[i]['contrast'] - (ye if i in e else yl if i in l else 0) for i in range(len(rows))]
    z = [(a * u, b * u) for (a, b), u in zip(x, residual)]
    meat = [[0., 0.], [0., 0.]]
    for t in range(len(rows)):
        for s in range(len(rows)):
            k = abs(t-s)
            if k <= lag:
                weight = 1-k/(lag+1)
                for a in range(2):
                    for b in range(2):
                        meat[a][b] += weight*z[t][a]*z[s][b]
    v = meat[0][0]/len(e)**2 + meat[1][1]/len(l)**2 - 2*meat[0][1]/(len(e)*len(l))
    return sqrt(max(v, 0.))


class JointHacReferenceTests(unittest.TestCase):
    def test_independent_sandwich_across_lags(self):
        start = date(2025, 9, 2)
        rows = [{'date': (start+timedelta(days=i)).isoformat(),
                 'contrast': float((i*7)%11 + (i>=13)*3 + (i%3)*0.25)} for i in range(30)]
        early = (rows[0]['date'], rows[11]['date'])
        late = (rows[15]['date'], rows[29]['date'])
        result = joint_window_hac(rows, early, late, lags=(0, 1, 3, 8))
        for lag, actual in result['hac_standard_errors'].items():
            with self.subTest(lag=lag):
                self.assertAlmostEqual(actual, reference(rows, early, late, lag), places=11)

    def test_constant_windows_zero_uncertainty(self):
        start = date(2025, 9, 1)
        rows = [{'date': (start+timedelta(days=i)).isoformat(),
                 'contrast': float(2 if i < 10 else 8)} for i in range(20)]
        early = (rows[0]['date'], rows[9]['date'])
        late = (rows[10]['date'], rows[19]['date'])
        r = joint_window_hac(rows, early, late, lags=(0, 1, 3))
        self.assertEqual(r['late_minus_early'], 6.)
        self.assertEqual(r['hac_standard_errors'], {0: 0., 1: 0., 3: 0.})

if __name__ == '__main__':
    unittest.main()
