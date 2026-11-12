"""Read-only diagnostics on published Phase 130 summaries, NOT raw-data replication."""
import csv
import json
from decimal import Decimal
from pathlib import Path

def unique_rows(path):
    with Path(path).open(encoding='utf-8', newline='') as stream:
        rows = list(csv.DictReader(stream))
    if len(rows) != 2 or {r['outcome'] for r in rows} != {'count', 'volume'}:
        raise ValueError('expected exactly one count and one volume row')
    return {r['outcome']: r for r in rows}

def audit(summary_file, sensitivity_file):
    summaries, groups = unique_rows(summary_file), unique_rows(sensitivity_file)
    output = {}
    for outcome in ('count', 'volume'):
        s, g = summaries[outcome], groups[outcome]
        d = Decimal(s['nov_minus_oct_pp'])
        lo, hi = Decimal(g['group_bootstrap_ci_low']), Decimal(g['group_bootstrap_ci_high'])
        leave_lo, leave_hi = Decimal(g['leave_one_group_out_min']), Decimal(g['leave_one_group_out_max'])
        minimum, maximum = Decimal(s['pre_placebo_min_pp']), Decimal(s['pre_placebo_max_pp'])
        n = int(s['pre_placebo_n'])
        directional = int(s['pre_placebo_at_least_as_negative'])
        absolute = int(s['pre_placebo_at_least_as_extreme_absolute'])
        if not (n > 0 and 0 <= directional <= n and 0 <= absolute <= n):
            raise ValueError('invalid placebo frequencies')
        if not (minimum <= maximum and minimum <= d <= maximum):
            raise ValueError('reported contrast outside placebo range')
        if not (lo <= hi and leave_lo <= leave_hi and leave_lo <= d <= leave_hi):
            raise ValueError('invalid group sensitivity range')
        if not (lo <= d <= hi):
            raise ValueError('contrast outside bootstrap interval')
        output[outcome] = {
            'contrast_pp': str(d),
            'bootstrap_includes_zero': lo <= 0 <= hi,
            'leave_one_group_out_same_sign': (leave_hi < 0 if d < 0 else leave_lo > 0),
            'leave_one_group_out_range_pp': [str(leave_lo), str(leave_hi)],
            'historical_placebo_range_pp': [str(minimum), str(maximum)],
            'absolute_extreme_fraction_descriptive': f'{absolute}/{n}',
            'at_least_as_negative_fraction_descriptive': f'{directional}/{n}',
        }
    if not output['count']['contrast_pp'].startswith('-') or Decimal(output['volume']['contrast_pp']) <= 0:
        raise ValueError('expected opposite signs in frozen tables')
    return output

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('summary')
    parser.add_argument('sensitivity')
    args = parser.parse_args()
    print(json.dumps(audit(args.summary, args.sensitivity), indent=2))
