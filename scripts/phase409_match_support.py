"""Matched group-date and exchange-date support audit; structural only."""
import csv
import json
import sys
from collections import defaultdict
from datetime import date

REQUIRED = ('date', 'security', 'exchange', 'treated', 'match_group')

def audit(rows, expected_controls=3):
    cells = defaultdict(lambda: {0: set(), 1: set()})
    exchange_cells = defaultdict(lambda: {0: set(), 1: set()})
    roster = defaultdict(lambda: {0: set(), 1: set()})
    seen, errors = set(), []
    n = 0
    for n, row in enumerate(rows, 1):
        if any(not str(row.get(k, '')).strip() for k in REQUIRED):
            errors.append(f'row {n}: missing field')
            continue
        try:
            d = date.fromisoformat(row['date']).isoformat()
            t = int(row['treated'])
            if t not in (0, 1):
                raise ValueError()
        except (ValueError, TypeError):
            errors.append(f'row {n}: invalid date/treatment')
            continue
        s, e, g = (row[k].strip() for k in ('security', 'exchange', 'match_group'))
        key = (d, s, e)
        if key in seen:
            errors.append(f'row {n}: duplicate security-exchange-date')
        seen.add(key)
        cells[(d, g)][t].add(s)
        exchange_cells[(d, g, e)][t].add(s)
        roster[g][t].add(s)
    paired = sum(bool(v[0]) and bool(v[1]) for v in cells.values())
    full = sum(len(v[1]) == 1 and len(v[0]) == expected_controls for v in cells.values())
    exchange_paired = sum(bool(v[0]) and bool(v[1]) for v in exchange_cells.values())
    violations = sorted(g for g, v in roster.items()
                        if len(v[1]) != 1 or len(v[0]) != expected_controls)
    if not cells:
        errors.append('no valid cells')
    if violations:
        errors.append('non-1:3 rosters: ' + ','.join(violations))
    if paired != len(cells):
        errors.append('some group-dates lack treated/control coverage')
    return dict(status='BLOCKED' if errors else 'STRUCTURE_ONLY_NOT_AUTHENTICATED',
                rows=n, match_groups=len(roster), group_dates=len(cells),
                paired_group_dates=paired, complete_1_to_3_group_dates=full,
                exchange_group_dates=len(exchange_cells),
                paired_exchange_group_dates=exchange_paired,
                roster_violations=violations, errors=errors,
                source_authenticated=False, historical_treatment_authenticated=False,
                note='1:3 is an assumed design diagnostic, not authenticated matching')

def main(path):
    with open(path, newline='', encoding='utf-8-sig') as f:
        result = audit(csv.DictReader(f))
    print(json.dumps(result, indent=2, sort_keys=True))
    return 2 if result['status'] == 'BLOCKED' else 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
