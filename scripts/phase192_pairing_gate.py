"""Structural count/volume pairing and fixed security/exchange roster audit; not causal."""
import csv
import json
import math
import sys
from collections import defaultdict
from datetime import date

FIELDS = ('security_id', 'exchange', 'trade_date', 'matched_group_id', 'outcome', 'contrast_pp')

def audit(rows):
    seen = set()
    outcomes = defaultdict(set)
    roster = defaultdict(set)
    dates = set()
    for row in rows:
        if set(row) != set(FIELDS):
            raise ValueError('schema mismatch')
        security, exchange, day, group, outcome = (row[k] for k in FIELDS[:-1])
        if any(not isinstance(v, str) or not v or v.strip() != v for v in (security, exchange, day, group, outcome)):
            raise ValueError('invalid identifier')
        try:
            if date.fromisoformat(day).isoformat() != day or date.fromisoformat(day).weekday() >= 5:
                raise ValueError('invalid trading weekday')
            if not math.isfinite(float(row['contrast_pp'])):
                raise ValueError('nonfinite contrast')
        except (TypeError, ValueError) as exc:
            raise ValueError('invalid date or contrast') from exc
        if outcome not in ('count', 'volume'):
            raise ValueError('invalid outcome')
        key = (security, exchange, day, group, outcome)
        if key in seen:
            raise ValueError('duplicate observation')
        seen.add(key)
        unit = (security, exchange, group)
        outcomes[(day, unit)].add(outcome)
        roster[day].add(unit)
        dates.add(day)
    if not seen:
        raise ValueError('empty panel')
    incomplete = [(day, unit) for (day, unit), values in outcomes.items() if values != {'count', 'volume'}]
    common = set.intersection(*(roster[d] for d in dates))
    union = set.union(*(roster[d] for d in dates))
    stable = all(roster[d] == union for d in dates)
    return {'dates': len(dates), 'rows': len(seen), 'distinct_units': len(union),
            'common_units': len(common), 'unpaired_unit_dates': len(incomplete),
            'roster_stable': stable, 'outcomes_paired': not incomplete,
            'eligible_for_fixed_roster_common_date_analysis': not incomplete and stable,
            'warning': 'Structural checks only; market calendar, source provenance and treatment still require independent authentication'}

def load(path):
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        if tuple(reader.fieldnames or ()) != FIELDS:
            raise ValueError('CSV header mismatch')
        return audit(list(reader))

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('usage: python phase192_pairing_gate.py panel.csv')
    print(json.dumps(load(sys.argv[1]), indent=2))
