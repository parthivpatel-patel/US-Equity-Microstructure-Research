"""Fail-closed fixed-roster audit; structural checks do not authenticate SEC data."""
from collections import defaultdict
from datetime import date
from math import isfinite

REQUIRED = ('date', 'security', 'exchange', 'group', 'treatment', 'outcome', 'value')

def audit_fixed_roster(rows, sessions, outcomes=('count', 'volume')):
    errors = set()
    rows, sessions, outcomes = list(rows), list(sessions), list(outcomes)
    if not rows: errors.add('empty_panel')
    if not sessions: errors.add('empty_calendar')
    if not outcomes or len(set(outcomes)) != len(outcomes): errors.add('invalid_outcomes')
    if len(sessions) != len(set(sessions)): errors.add('duplicate_calendar')
    if sessions != sorted(sessions): errors.add('unordered_calendar')
    for s in sessions:
        try:
            if type(s) is not str or date.fromisoformat(s).isoformat() != s: raise ValueError
        except ValueError: errors.add('invalid_calendar_date')
    if any(type(o) is not str or not o for o in outcomes): errors.add('invalid_outcomes')
    seen = set(); identities = defaultdict(set); groups = defaultdict(set)
    roster = set(); observed = set()
    for row in rows:
        if not isinstance(row, dict) or any(k not in row for k in REQUIRED):
            errors.add('malformed_row'); continue
        d,sec,ex,g,t,o,v = (row[k] for k in REQUIRED)
        if any(type(x) is not str or not x for x in (d,sec,ex,g,o)):
            errors.add('invalid_identifier'); continue
        try:
            if date.fromisoformat(d).isoformat() != d: raise ValueError
        except ValueError: errors.add('invalid_date')
        if type(t) is not int or t not in (0,1): errors.add('invalid_treatment')
        if type(v) not in (int,float) or not isfinite(v): errors.add('invalid_value')
        if d not in sessions: errors.add('unexpected_date')
        if o not in outcomes: errors.add('unexpected_outcome')
        key = (d,sec,ex,o)
        if key in seen: errors.add('duplicate_cell')
        seen.add(key); observed.add(key); roster.add((sec,ex))
        identities[sec,ex].add((g,t)); groups[g].add(t)
    if any(len(assignments) != 1 for assignments in identities.values()):
        errors.add('identity_switch')
    if any(arms != {0,1} for arms in groups.values()): errors.add('unmatched_group')
    expected = {(d,sec,ex,o) for d in sessions for sec,ex in roster for o in outcomes}
    missing = expected - observed
    if missing: errors.add('missing_cells')
    return {'admitted': not errors, 'errors': sorted(errors), 'row_count': len(rows),
            'roster_size': len(roster), 'expected_cells': len(expected),
            'observed_unique_cells': len(observed), 'missing_cells': len(missing),
            'treatment_authenticated': False, 'source_authenticated': False}
