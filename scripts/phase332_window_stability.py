"""Descriptive Phase 131 window stability audit; not causal inference."""
import csv
import json
import sys
from decimal import Decimal

def audit(path):
    with open(path, newline='', encoding='utf-8') as stream:
        rows = list(csv.DictReader(stream))
    if not rows:
        raise ValueError('empty input')
    grouped = {}
    for row in rows:
        outcome = row['outcome']
        days = int(row['window_days'])
        n = int(row['pre_placebo_count'])
        negative = int(row['pre_placebo_at_least_as_negative'])
        extreme = int(row['pre_placebo_at_least_as_extreme_abs'])
        contrast = Decimal(row['nov_minus_oct_pp'])
        if not (days > 0 and n > 0 and 0 <= negative <= extreme <= n and contrast.is_finite()):
            raise ValueError('invalid row')
        if days in grouped.setdefault(outcome, {}):
            raise ValueError('duplicate outcome/window')
        grouped[outcome][days] = (contrast, n, negative, extreme)
    result = {}
    for outcome, windows in sorted(grouped.items()):
        ordered = sorted(windows.items())
        contrasts = [v[0] for _, v in ordered]
        if any(x == 0 for x in contrasts):
            raise ValueError('zero contrast: sign audit undefined')
        result[outcome] = {
            'windows': [{'days': days, 'contrast_pp': str(v[0]), 'placebo_n': v[1],
                         'negative_tail_fraction': f'{v[2]}/{v[1]}',
                         'absolute_tail_fraction': f'{v[3]}/{v[1]}'}
                        for days, v in ordered],
            'positive_window_count': sum(x > 0 for x in contrasts),
            'negative_window_count': sum(x < 0 for x in contrasts),
            'sign_stable': all(x > 0 for x in contrasts) or all(x < 0 for x in contrasts),
            'contrast_range_pp': str(max(contrasts) - min(contrasts)),
            'window_sample_count_nonincreasing': all(a[1][1] >= b[1][1] for a,b in zip(ordered,ordered[1:]))
        }
    return result

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('usage: python scripts/phase332_window_stability.py results/phase131_window_sensitivity.csv')
    print(json.dumps(audit(sys.argv[1]), indent=2))
