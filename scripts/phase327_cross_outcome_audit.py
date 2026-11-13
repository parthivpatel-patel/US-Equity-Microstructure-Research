"""Cross-outcome provenance diagnostics for dated placebo windows (stdlib only)."""
import csv
import datetime as dt
import json
import sys
from collections import defaultdict
from decimal import Decimal, InvalidOperation

REQUIRED = {'outcome', 'window_id', 'start_date', 'end_date', 'placebo_pp'}
REFORM = dt.date(2025, 11, 3)

def audit(rows):
    groups = defaultdict(dict)
    for row in rows:
        if not REQUIRED.issubset(row):
            raise ValueError('missing columns')
        outcome, wid = row['outcome'].strip(), row['window_id'].strip()
        if not outcome or not wid or wid in groups[outcome]:
            raise ValueError('missing or duplicate identity')
        a, b = dt.date.fromisoformat(row['start_date']), dt.date.fromisoformat(row['end_date'])
        if a > b or b >= REFORM:
            raise ValueError('invalid or post-reform placebo interval')
        try:
            x = Decimal(row['placebo_pp'])
        except InvalidOperation as exc:
            raise ValueError('invalid numeric placebo') from exc
        if not x.is_finite():
            raise ValueError('nonfinite placebo')
        groups[outcome][wid] = (a, b, x)
    if not groups:
        raise ValueError('no windows')
    outcomes = sorted(groups)
    diagnostics = {}
    for i, left in enumerate(outcomes):
        for right in outcomes[i+1:]:
            a, b = groups[left], groups[right]
            common = set(a) & set(b)
            disagreements = sorted(wid for wid in common if a[wid][:2] != b[wid][:2])
            diagnostics[f'{left}|{right}'] = {
                'left_windows': len(a), 'right_windows': len(b),
                'shared_ids': len(common),
                'only_left': sorted(set(a)-set(b)),
                'only_right': sorted(set(b)-set(a)),
                'shared_id_date_disagreements': disagreements,
                'same_window_identity_and_dates': len(a)==len(b)==len(common) and not disagreements,
                'interpretation': 'Diagnostic only: different outcome-specific samples may be intentional; verify producer and filters.'
            }
    return {'outcomes': {k: len(v) for k,v in sorted(groups.items()}, 'pairwise': diagnostics}

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit('usage: python scripts/phase327_cross_outcome_audit.py dated_windows.csv')
    with open(sys.argv[1], newline='') as f:
        print(json.dumps(audit(list(csv.DictReader(f))), indent=2, sort_keys=True))
