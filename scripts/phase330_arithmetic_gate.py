"""Aggregate arithmetic and duplicate-key gate; no raw-data authentication."""
import csv
import json
import sys
from decimal import Decimal, InvalidOperation

def read(path):
    with open(path, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def check(summary, windows, tolerance=Decimal('0.0000015')):
    if tolerance < 0: raise ValueError('negative tolerance')
    out=[]
    seen=set()
    for row in windows:
        key=(row['outcome'],row['window_days'])
        if key in seen: raise ValueError('duplicate window key: '+str(key))
        seen.add(key)
        try:
            nov=Decimal(row['november_pp']); oct_=Decimal(row['october6_pp']); reported=Decimal(row['nov_minus_oct_pp'])
        except InvalidOperation as e: raise ValueError('invalid decimal') from e
        if not all(v.is_finite() for v in (nov,oct_,reported)): raise ValueError('nonfinite value')
        error=reported-(nov-oct_)
        n=int(row['pre_placebo_count']); negative=int(row['pre_placebo_at_least_as_negative']); extreme=int(row['pre_placebo_at_least_as_extreme_abs'])
        if n < 1 or not (0 <= negative <= n and 0 <= extreme <= n): raise ValueError('invalid count')
        subset_ok=reported>=0 or negative<=extreme
        out.append({'outcome':row['outcome'],'window_days':int(row['window_days']), 'arithmetic_error_pp':str(error), 'arithmetic_ok':abs(error)<=tolerance,'negative_tail_subset_ok':subset_ok})
    return out

if __name__=='__main__':
    if len(sys.argv)!=3: raise SystemExit('usage: python scripts/phase330_arithmetic_gate.py results/phase130_summary.csv results/phase131_window_sensitivity.csv')
    results=check(read(sys.argv[1]),read(sys.argv[2]))
    print(json.dumps(results,indent=2))
    if not all(r['arithmetic_ok'] and r['negative_tail_subset_ok'] for r in results): sys.exit(1)
