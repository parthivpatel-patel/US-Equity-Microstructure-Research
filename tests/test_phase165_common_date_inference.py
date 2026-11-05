"""Common-date matched-group inference diagnostic; constructed fixtures only."""
import math
import random
import unittest
from collections import defaultdict

def date_contrasts(rows):
    """Require both arms for each matched group and date; average groups equally."""
    cells = defaultdict(lambda: {0: [], 1: []})
    for date, group, arm, outcome in rows:
        if arm not in (0, 1) or not math.isfinite(outcome):
            raise ValueError("invalid arm or outcome")
        cells[(date, group)][arm].append(outcome)
    by_date = defaultdict(list)
    for (date, group), arms in cells.items():
        if not arms[0] or not arms[1]:
            raise ValueError("incomplete matched-group/date cell")
        by_date[date].append(sum(arms[1])/len(arms[1])-sum(arms[0])/len(arms[0]))
    if not by_date:
        raise ValueError("empty panel")
    return {date: sum(v)/len(v) for date,v in sorted(by_date.items())}

def prepost_stat(contrasts, cutoff):
    pre = [v for d,v in contrasts.items() if d < cutoff]
    post = [v for d,v in contrasts.items() if d >= cutoff]
    if not pre or not post:
        raise ValueError("both periods required")
    return sum(post)/len(post)-sum(pre)/len(pre)

def moving_block_ci(contrasts, cutoff, block_length, draws=999, seed=0):
    """Noncircular date blocks separately resampled within each period."""
    dates = sorted(contrasts)
    pre = [contrasts[d] for d in dates if d < cutoff]
    post = [contrasts[d] for d in dates if d >= cutoff]
    if not pre or not post or block_length < 1 or draws < 1:
        raise ValueError("invalid periods, block length or draws")
    if block_length > min(len(pre),len(post)):
        raise ValueError("block longer than shorter period")
    rng = random.Random(seed)
    def sample(values):
        out = []
        while len(out) < len(values):
            start = rng.randrange(len(values)-block_length+1)
            out.extend(values[start:start+block_length])
        return out[:len(values)]
    estimates = sorted(sum(sample(post))/len(post)-sum(sample(pre))/len(pre)
                       for _ in range(draws))
    return estimates[int(.025*(draws-1))], estimates[int(.975*(draws-1))]

class CommonDateTests(unittest.TestCase):
    def test_group_date_average(self):
        rows=[("01","a",1,5.),("01","a",0,3.),
              ("01","b",1,7.),("01","b",0,3.)]
        self.assertEqual(date_contrasts(rows),{"01":3.})
    def test_incomplete_cell_rejected(self):
        with self.assertRaises(ValueError):
            date_contrasts([("01","a",1,5.)])
    def test_nonfinite_rejected(self):
        with self.assertRaises(ValueError):
            date_contrasts([("01","a",1,float("nan"))])
    def test_prepost(self):
        self.assertEqual(prepost_stat({"01":1.,"02":1.,"03":3.,"04":3.},"03"),2.)
    def test_common_shock_cancels(self):
        rows=[("01","a",1,102.),("01","a",0,100.),
              ("02","a",1,-98.),("02","a",0,-100.)]
        self.assertEqual(date_contrasts(rows),{"01":2.,"02":2.})
    def test_constant_bootstrap(self):
        c={str(i).zfill(2):(1. if i<5 else 3.) for i in range(10)}
        self.assertEqual(moving_block_ci(c,"05",2,99,12),(2.,2.))
    def test_seed_reproducible(self):
        c={str(i).zfill(2):float(i%4) for i in range(12)}
        self.assertEqual(moving_block_ci(c,"06",2,99,9),
                         moving_block_ci(c,"06",2,99,9))
    def test_overlong_block_rejected(self):
        with self.assertRaises(ValueError):
            moving_block_ci({"01":0.,"02":1.,"03":2.,"04":3.},"03",3)
    def test_missing_period_rejected(self):
        with self.assertRaises(ValueError):
            prepost_stat({"01":1.},"01")

if __name__=="__main__":
    unittest.main()
