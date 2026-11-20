import csv
import importlib.util
import tempfile
import unittest
from pathlib import Path

p = Path(__file__).resolve().parents[1] / 'scripts' / 'phase2_sensitivity_reaudit.py'
spec = importlib.util.spec_from_file_location('audit', p)
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


def row(ticker, treated, pre=0.2, post=0.3, vpre=0.1, vpost=0.2, trades=100):
    return dict(Ticker=ticker, treated=treated, r_pre=pre, r_post=post,
                v_pre=vpre, v_post=vpost, days_pre=23.0, days_post=19.0,
                trades_pre=float(trades), trades_post=float(trades),
                dr=post-pre, dv=vpost-vpre)


class Check(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / 'panel.csv'
        self.rows = [row('A', 1, post=.4, trades=100),
                     row('B', 1, post=.3, trades=200),
                     row('C', 0, post=.3, trades=150),
                     row('D', 0, post=.3, trades=300)]

    def tearDown(self): self.tmp.cleanup()

    def write(self, rows=None):
        with self.path.open('w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=audit.REQUIRED)
            writer.writeheader(); writer.writerows(rows if rows is not None else self.rows)

    def test_valid(self):
        self.write(); x, digest = audit.load(self.path)
        self.assertEqual(len(x),4)
        self.assertEqual(len(digest),64)
        self.assertEqual(audit.analyze(x)['n_treated'],2)

    def test_equal_diff(self):
        self.write(); x, _ = audit.load(self.path)
        z = audit.analyze(x)['scenarios'][0]
        self.assertAlmostEqual(z['hidden_trade_rate_diff_pp'], 5.0)

    def test_duplicate(self):
        self.write(self.rows + [self.rows[0]])
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            audit.load(self.path)

    def test_missing_cell(self):
        a = [r.copy() for r in self.rows]; a[0]['dr'] = ''
        self.write(a)
        with self.assertRaises(ValueError): audit.load(self.path)

    def test_nonfinite(self):
        a = [r.copy() for r in self.rows]; a[0]['r_pre'] = 'nan'
        self.write(a)
        with self.assertRaisesRegex(ValueError, 'Nonfinite'):
            audit.load(self.path)

    def test_diff_inconsistent(self):
        a = [r.copy() for r in self.rows]; a[0]['dr'] = .4
        self.write(a)
        with self.assertRaisesRegex(ValueError, 'mismatch'):
            audit.load(self.path)

    def test_invalid_treatment(self):
        a = [r.copy() for r in self.rows]; a[0]['treated'] = '2'
        self.write(a)
        with self.assertRaisesRegex(ValueError, 'treatment'):
            audit.load(self.path)

    def test_percentile(self):
        self.assertAlmostEqual(audit.percentile([1, 2, 3, 4], .25), 1.75)

    def test_effective_n(self):
        self.assertAlmostEqual(audit.eff_n([{'w':1},{'w':1}], 'w'),2)

    def test_rate_limit(self):
        a = [r.copy() for r in self.rows]; a[0]['r_post'] = 1.5
        self.write(a)
        with self.assertRaisesRegex(ValueError, 'rate'):
            audit.load(self.path)


if __name__ == '__main__': unittest.main()
