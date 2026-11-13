#!/usr/bin/env python3
"""Sharp covariance-agnostic SE bounds for differences in published period slopes.

Input: Phase 136 aggregate presentation, NOT authenticated SEC observations.
Cauchy-Schwarz: |s1-s2| <= SE(b1-b2) <= s1+s2.
"""
import csv
import json
import sys
from decimal import Decimal, InvalidOperation

OUTCOMES = ('count', 'volume')
LAGS = (0, 3, 5, 10, 15)
PERIODS = ('Jul-Sep', 'Jul-Oct')
EXPECTED = {(o, p, l) for o in OUTCOMES for p in PERIODS for l in LAGS}

def audit(rows):
    cells = {}
    for r in rows:
        try:
            key = (r['outcome'], r['period'], int(r['hac_lag']))
            slope = Decimal(r['slope_pp_per_trading_day'])
            se = Decimal(r['two_way_se'])
            dates, groups = int(r['dates']), int(r['groups'])
        except (KeyError, ValueError, InvalidOperation) as exc:
            raise ValueError('invalid row') from exc
        if key not in EXPECTED or key in cells:
            raise ValueError('duplicate or unexpected cell')
        if not slope.is_finite() or not se.is_finite() or se <= 0 or dates < 2 or groups < 2:
            raise ValueError('invalid value')
        cells[key] = (slope, se, dates, groups)
    if set(cells) != EXPECTED:
        raise ValueError('incomplete grid')
    out = []
    for outcome in OUTCOMES:
        for period in PERIODS:
            values = [cells[outcome, period, lag] for lag in LAGS]
            if len({(v[0], v[2], v[3]) for v in values}) != 1:
                raise ValueError('slope or sample size varies across lag')
        for lag in LAGS:
            early, late = (cells[outcome, p, lag] for p in PERIODS)
            delta = late[0] - early[0]
            lo, hi = abs(early[1]-late[1]), early[1]+late[1]
            out.append({
                'outcome': outcome, 'lag': lag,
                'jul_oct_minus_jul_sep_slope_pp_per_day': str(delta),
                'se_lower_bound': str(lo), 'se_upper_bound': str(hi),
                'minimum_abs_slope_change_over_se': str(round(abs(delta)/hi, 6)),
                'guaranteed_above_illustrative_1_96': abs(delta) > Decimal('1.96')*hi,
                'sample_dates_jul_sep': early[2], 'sample_dates_jul_oct': late[2],
                'groups_jul_sep': early[3], 'groups_jul_oct': late[3]
            })
    return out

if __name__ == '__main__':
    with open(sys.argv[1], newline='', encoding='utf-8') as f:
        print(json.dumps(audit(csv.DictReader(f)), indent=2))
