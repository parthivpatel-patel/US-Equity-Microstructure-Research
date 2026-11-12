"""Audit descriptive placebo-count semantics from frozen Phase 130 CSV; no raw-data inference."""
import csv
import json
from decimal import Decimal, InvalidOperation
from pathlib import Path

REQUIRED = {'outcome', 'nov_minus_oct_pp', 'pre_placebo_n',
            'pre_placebo_at_least_as_negative', 'pre_placebo_at_least_as_extreme_absolute',
            'pre_placebo_min_pp', 'pre_placebo_max_pp'}

def audit(path):
    with Path(path).open(newline='', encoding='utf-8') as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames is None or len(reader.fieldnames) != len(set(reader.fieldnames)) or not REQUIRED.issubset(reader.fieldnames):
            raise ValueError('missing or duplicate CSV columns')
        rows = list(reader)
    if len(rows) != 2 or {r['outcome'] for r in rows} != {'count', 'volume'}:
        raise ValueError('expected one count and one volume outcome')
    result = {}
    for r in rows:
        try:
            d, low, high = (Decimal(r[k]) for k in ('nov_minus_oct_pp', 'pre_placebo_min_pp', 'pre_placebo_max_pp'))
            n, negative, absolute = (int(r[k]) for k in ('pre_placebo_n', 'pre_placebo_at_least_as_negative', 'pre_placebo_at_least_as_extreme_absolute'))
        except (InvalidOperation, ValueError) as exc:
            raise ValueError('invalid numeric field') from exc
        if not all(x.is_finite() for x in (d, low, high)) or not low <= high or n <= 0 or not (0 <= negative <= n and 0 <= absolute <= n):
            raise ValueError('invalid placebo summary')
        if not low <= d <= high:
            raise ValueError('event contrast outside reported historical range')
        # If d < 0, every placebo <= d is also at least as extreme in absolute value.
        if d < 0 and absolute < negative:
            raise ValueError('incompatible negative-tail and absolute counts')
        result[r['outcome']] = {
            'contrast_pp': str(d), 'historical_windows': n,
            'negative_tail_count': negative, 'absolute_extreme_count': absolute,
            'negative_tail_share': f'{negative}/{n}',
            'absolute_extreme_share': f'{absolute}/{n}',
            'absolute_minus_negative_count': absolute - negative,
            'calibrated_p_value': None,
        }
    return result

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('summary_csv')
    print(json.dumps(audit(parser.parse_args().summary_csv), indent=2))
