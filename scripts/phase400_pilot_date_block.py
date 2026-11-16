"""Descriptive common-date block bootstrap for recovered round-lot pilot tiers."""
import argparse
import json
import numpy as np
import pandas as pd

def audit(df):
    fields = ['Date', 'lot', 'Hidden', 'TradesForHidden', "HiddenVol('000)", "TradeVolForHidden('000)"]
    if df[fields].isna().any().any() or df.duplicated(['Date', 'lot']).any():
        raise ValueError('missing cells or duplicate tier-date')
    if set(df.lot.astype(int)) != {10, 40, 100} or df.groupby('Date').lot.nunique().ne(3).any():
        raise ValueError('incomplete tiers/dates')
    for n, d in [('Hidden', 'TradesForHidden'), ("HiddenVol('000)", "TradeVolForHidden('000)")]:
        if ((df[n] < 0) | (df[d] <= 0) | (df[n] > df[d])).any():
            raise ValueError('invalid numerator/denominator')

def contrast(df, num, den, group):
    x = df.copy()
    x['grp'] = np.where(x.lot.eq(100), 'control', 'reduced') if group == 'pooled' else x.lot.astype(int).astype(str)
    s = x.groupby('grp')[[num, den]].sum()
    rates = s[num] / s[den]
    return float(rates['reduced'] - rates['control']) if group == 'pooled' else float(rates['10'] - rates['100'])

def resample(df, rng, block):
    dates = np.array(sorted(df.Date.unique()))
    n = len(dates)
    indices = []
    while len(indices) < n:
        start = int(rng.integers(0, n))
        indices.extend((start + np.arange(block)) % n)
    return pd.concat([df[df.Date.eq(d)] for d in dates[np.array(indices[:n])]], ignore_index=True)

def run(df, reps=1000, block=5, seed=400):
    audit(df)
    if reps < 1 or block < 1:
        raise ValueError('positive repetitions/block required')
    masks = {'early_oct': df.Date.between(20251001, 20251015),
             'late_oct': df.Date.between(20251016, 20251031),
             'nov': df.Date.ge(20251103)}
    parts = {k: df.loc[v].copy() for k, v in masks.items()}
    if any(v.empty for v in parts.values()):
        raise ValueError('empty period')
    rng = np.random.default_rng(seed)
    out = []
    for metric, (num, den) in {'trade': ('Hidden', 'TradesForHidden'),
                              'volume': ("HiddenVol('000)", "TradeVolForHidden('000)")}.items():
        for group in ['pooled', '10_vs_100']:
            observed = {k: contrast(v, num, den, group) for k, v in parts.items()}
            draws = {'oct_placebo': [], 'nov_vs_late_oct': []}
            for _ in range(reps):
                sampled = {k: resample(v, rng, block) for k, v in parts.items()}
                vals = {k: contrast(v, num, den, group) for k, v in sampled.items()}
                draws['oct_placebo'].append(vals['late_oct'] - vals['early_oct'])
                draws['nov_vs_late_oct'].append(vals['nov'] - vals['late_oct'])
            for label, value in [('oct_placebo', observed['late_oct'] - observed['early_oct']),
                                 ('nov_vs_late_oct', observed['nov'] - observed['late_oct'])]:
                low, high = np.quantile(draws[label], [.025, .975])
                out.append({'metric': metric, 'group': group, 'comparison': label,
                            'estimate_pp': 100 * value, 'bootstrap_percentile_low_pp': 100 * float(low),
                            'bootstrap_percentile_high_pp': 100 * float(high),
                            'draws': reps, 'block_sessions': block})
    return out

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('csv')
    parser.add_argument('--reps', type=int, default=1000)
    args = parser.parse_args()
    print(json.dumps(run(pd.read_csv(args.csv), args.reps), indent=2))
