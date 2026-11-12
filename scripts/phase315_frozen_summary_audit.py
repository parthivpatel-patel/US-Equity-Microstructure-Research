"""Audit arithmetic of frozen Phase 130 summaries; not source-data authentication."""
import csv
from decimal import Decimal
from pathlib import Path

def audit(summary_path, sensitivity_path):
    with Path(summary_path).open(newline='', encoding='utf-8') as f:
        summary = {r['outcome']: r for r in csv.DictReader(f)}
    with Path(sensitivity_path).open(newline='', encoding='utf-8') as f:
        sensitivity = {r['outcome']: r for r in csv.DictReader(f)}
    if set(summary) != {'count', 'volume'} or set(sensitivity) != set(summary):
        raise ValueError('unexpected outcome keys')
    result = {}
    for outcome, r in summary.items():
        s = sensitivity[outcome]
        nov, oct, diff = (Decimal(r[k]) for k in ('november_pp', 'october_pp', 'nov_minus_oct_pp'))
        group_diff = Decimal(s['difference_pp'])
        if abs((nov - oct) - diff) > Decimal('1e-12') or abs(diff - group_diff) > Decimal('1e-12'):
            raise ValueError(f'{outcome}: difference inconsistency')
        n = int(r['pre_placebo_n'])
        negative = int(r['pre_placebo_at_least_as_negative'])
        absolute = int(r['pre_placebo_at_least_as_extreme_absolute'])
        if not (n > 0 and 0 <= negative <= n and 0 <= absolute <= n):
            raise ValueError(f'{outcome}: invalid placebo counts')
        low, high = Decimal(s['group_bootstrap_ci_low']), Decimal(s['group_bootstrap_ci_high'])
        if low > high or not low <= group_diff <= high:
            raise ValueError(f'{outcome}: inconsistent interval')
        result[outcome] = {
            'november_pp': str(nov), 'october_pp': str(oct),
            'nov_minus_oct_pp': str(diff), 'group_bootstrap_ci_low': str(low),
            'group_bootstrap_ci_high': str(high), 'ci_includes_zero': low <= 0 <= high,
            'placebo_extreme_absolute_count': absolute, 'placebo_window_count': n,
            'descriptive_extreme_fraction': f'{absolute}/{n}',
            'caveat': 'Overlapping/post-hoc placebo windows: fraction is NOT a calibrated p-value.'
        }
    return result

if __name__ == '__main__':
    import argparse, json
    p = argparse.ArgumentParser()
    p.add_argument('summary')
    p.add_argument('sensitivity')
    args = p.parse_args()
    print(json.dumps(audit(args.summary, args.sensitivity), indent=2))
