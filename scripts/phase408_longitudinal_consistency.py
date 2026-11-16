"""Fail-closed longitudinal identity and matched-pair integrity checks.

Does not authenticate SEC data or historical round-lot treatment.
Usage: python phase408_longitudinal_consistency.py panel.csv
"""
import csv
import json
import sys
from collections import defaultdict
from datetime import date

REQUIRED = ('date', 'security', 'exchange', 'treated', 'match_group')

def audit(rows):
    rows = list(rows)
    errors = []
    identity = defaultdict(set)
    membership = defaultdict(set)
    daily_groups = defaultdict(lambda: defaultdict(set))
    keys = set()
    dates = set()
    for n, row in enumerate(rows, 2):
        if any(not str(row.get(k, '')).strip() for k in REQUIRED):
            errors.append(f'row {n}: missing required identity field')
            continue
        try:
            d = date.fromisoformat(row['date'])
            t = int(row['treated'])
            if t not in (0, 1):
                raise ValueError('not binary')
        except (TypeError, ValueError):
            errors.append(f'row {n}: invalid date or treatment')
            continue
        s, e, g = (row[k].strip() for k in ('security', 'exchange', 'match_group'))
        key = (d, s, e)
        if key in keys:
            errors.append(f'row {n}: duplicate security-exchange-date')
        keys.add(key)
        identity[s].add(t)
        membership[s].add(g)
        daily_groups[(d, g)][t].add(s)
        dates.add(d)
    for s, treatments in sorted(identity.items()):
        if len(treatments) > 1:
            errors.append(f'security {s}: treatment changes across dates/exchanges')
    for s, groups in sorted(membership.items()):
        if len(groups) > 1:
            errors.append(f'security {s}: match group changes across dates/exchanges')
    group_rosters = defaultdict(lambda: defaultdict(set))
    for (d, g), sides in daily_groups.items():
        for t, securities in sides.items():
            group_rosters[g][t].update(securities)
    for g, sides in sorted(group_rosters.items()):
        if not sides[0] or not sides[1]:
            errors.append(f'match group {g}: lacks treated or control security')
    paired_days = sum(bool(sides[0]) and bool(sides[1]) for sides in daily_groups.values())
    unpaired_days = sum(not (sides[0] and sides[1]) for sides in daily_groups.values())
    if unpaired_days:
        errors.append(f'{unpaired_days} match-group-date cells lack simultaneous treated/control coverage')
    if not identity:
        errors.append('no valid observations')
    return {
        'status': 'BLOCKED' if errors else 'LONGITUDINAL_STRUCTURE_PASS_NOT_AUTHENTICATED',
        'rows': len(rows), 'securities': len(identity), 'dates': len(dates),
        'match_groups': len(group_rosters), 'paired_group_dates': paired_days,
        'unpaired_group_dates': unpaired_days, 'errors': errors,
        'authentication': 'NOT_VERIFIED', 'causal_identification': 'NOT_ESTABLISHED',
        'scope_note': 'No source provenance, September coverage, treatment historical truth, or inference verified.'
    }

def main(path):
    with open(path, newline='', encoding='utf-8-sig') as f:
        result = audit(csv.DictReader(f))
    print(json.dumps(result, indent=2, sort_keys=True))
    return 2 if result['errors'] else 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
