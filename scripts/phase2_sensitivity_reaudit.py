#!/usr/bin/env python3
"""Audit archived Phase-2 SEC-derived *processed* stock panel, without publishing input rows.

This is an exploratory reanalysis, NOT an original-SEC authentication or causal estimate.
Usage: python phase2_sensitivity_reaudit.py path/to/roundlot_phase2_security_panel.csv
"""
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path

REQUIRED = ('Ticker', 'treated', 'r_post', 'r_pre', 'v_post', 'v_pre',
            'days_post', 'days_pre', 'trades_post', 'trades_pre', 'dr', 'dv')
NUMERIC = REQUIRED[2:]


def load(path):
    raw = Path(path).read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    with Path(path).open(newline='', encoding='utf-8-sig') as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames is None or set(reader.fieldnames) != set(REQUIRED):
            raise ValueError('Unexpected panel header')
        rows, seen = [], set()
        for line, r in enumerate(reader, 2):
            if None in r or None in r.values():
                raise ValueError(f'Malformed CSV line {line}')
            ticker = r['Ticker']
            if not ticker or ticker in seen:
                raise ValueError(f'Duplicate/blank ticker on line {line}')
            seen.add(ticker)
            if r['treated'] not in ('0', '1'):
                raise ValueError(f'Invalid treatment indicator on line {line}')
            row = {'Ticker': ticker, 'treated': int(r['treated'])}
            for k in NUMERIC:
                try:
                    row[k] = float(r[k])
                except (TypeError, ValueError):
                    raise ValueError(f'Invalid {k} on line {line}') from None
                if not math.isfinite(row[k]):
                    raise ValueError(f'Nonfinite {k} on line {line}')
            if any(not 0 <= row[k] <= 1 for k in ('r_pre', 'r_post', 'v_pre', 'v_post')):
                raise ValueError(f'Invalid rate on line {line}')
            if any(row[k] <= 0 for k in ('trades_pre', 'trades_post', 'days_pre', 'days_post')):
                raise ValueError(f'Invalid denominator on line {line}')
            if abs(row['dr'] - (row['r_post'] - row['r_pre'])) > 1e-10 or \
               abs(row['dv'] - (row['v_post'] - row['v_pre'])) > 1e-10:
                raise ValueError(f'Rate-difference mismatch on line {line}')
            rows.append(row)
    if {x['treated'] for x in rows} != {0, 1}:
        raise ValueError('Both treated and control groups required')
    return rows, digest


def percentile(values, p):
    a = sorted(values)
    if not a: raise ValueError('Empty quantile')
    t = (len(a) - 1) * p
    lo = int(t); hi = min(lo + 1, len(a) - 1)
    return a[lo] + (t - lo) * (a[hi] - a[lo])


def mean(rows, col, weight=None):
    w = [r[weight] if weight else 1.0 for r in rows]
    return math.fsum(r[col] * wi for r, wi in zip(rows, w)) / math.fsum(w)


def eff_n(rows, weight):
    w = [r[weight] for r in rows]
    return math.fsum(w)**2 / math.fsum(x*x for x in w)


def analyze(rows):
    t = [r for r in rows if r['treated'] == 1]
    c = [r for r in rows if r['treated'] == 0]
    q1_t = percentile([r['trades_pre'] for r in t], .25)
    q1_c = percentile([r['trades_pre'] for r in c], .25)
    lo, hi = min(r['trades_pre'] for r in t), max(r['trades_pre'] for r in t)
    days_pre = max(r['days_pre'] for r in rows)
    days_post = max(r['days_post'] for r in rows)
    cases = [
        ('equal_security', t, c, None),
        ('baseline_trade_count_weighted', t, c, 'trades_pre'),
        ('within_arm_upper_75pct_baseline_trades',
         [r for r in t if r['trades_pre'] >= q1_t],
         [r for r in c if r['trades_pre'] >= q1_c], None),
        ('max_days_both_periods',
         [r for r in t if r['days_pre'] == days_pre and r['days_post'] == days_post],
         [r for r in c if r['days_pre'] == days_pre and r['days_post'] == days_post], None),
        ('treated_trade_range_overlap', t,
         [r for r in c if lo <= r['trades_pre'] <= hi], None),
    ]
    scenarios = []
    for name, treated, controls, weights in cases:
        if not treated or not controls:
            raise ValueError('Selection emptied a comparison arm: ' + name)
        scenarios.append({
            'scenario': name, 'n_treated': len(treated), 'n_control': len(controls),
            'hidden_trade_rate_diff_pp': (mean(treated, 'dr', weights) - mean(controls, 'dr', weights))*100,
            'hidden_volume_rate_diff_pp': (mean(treated, 'dv', weights) - mean(controls, 'dv', weights))*100,
        })
    return {
        'scope': 'processed Phase-2 panel only; no raw SEC verification, no causal interpretation',
        'n_securities': len(rows), 'n_treated': len(t), 'n_control': len(c),
        'baseline_treated_minus_control': {
            'hidden_trade_rate_pp': 100 * (mean(t,'r_pre') - mean(c,'r_pre')),
            'hidden_volume_rate_pp': 100 * (mean(t,'v_pre') - mean(c,'v_pre')),
        },
        'baseline_trade_weight_effective_n': {
            'treated': eff_n(t,'trades_pre'), 'control': eff_n(c,'trades_pre')
        },
        'scenarios': scenarios,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('panel')
    ap.add_argument('--expect-sha256', help='Require an exact archived processed-panel SHA-256')
    args = ap.parse_args()
    rows, sha = load(args.panel)
    if args.expect_sha256 and sha.lower() != args.expect_sha256.lower():
        raise SystemExit('Source-file SHA-256 mismatch; refusing analysis')
    out = analyze(rows)
    out['input_sha256'] = sha
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
