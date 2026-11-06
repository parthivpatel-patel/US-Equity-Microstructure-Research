"""Fail-closed admission wrapper for the Phase 198 count/volume pairing audit.

Structural checks do not authenticate historical SEC observations or treatment.
"""
from collections import Counter
from scripts.phase198_pair_consistency import audit


def admit(rows, expected_windows):
    rows = list(rows)
    expected = list(expected_windows)
    if not expected or len(expected) != len(set(expected)) or any(
        not isinstance(w, str) or not w.strip() for w in expected
    ):
        raise ValueError('expected_windows must contain unique nonblank names')
    if not rows:
        return {'admitted': False, 'reasons': ['empty_panel'], 'counts': {}, 'audit': audit(rows)}
    result = audit(rows)
    counts = dict(sorted(Counter(r['window'] for r in rows).items()))
    reasons = []
    if set(counts) != set(expected):
        reasons.append('window_mismatch')
    if result['unpaired_entity_dates']:
        reasons.append('unpaired_entity_dates')
    if result['within_pair_assignment_conflicts']:
        reasons.append('within_pair_assignment_conflicts')
    return {'admitted': not reasons, 'reasons': reasons, 'counts': counts, 'audit': result}
