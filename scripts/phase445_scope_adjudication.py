"""Adjudicate security-only membership flags without overriding support checks.

Inputs must be Phase 432 daily and Phase 442 assignment reports bound to identical bytes.
No SEC authentication or causal estimation.
"""
def adjudicate(daily, assignment):
    if not isinstance(daily, dict) or not isinstance(assignment, dict):
        raise ValueError('reports must be dictionaries')
    for key in ('source_sha256', 'source_bytes', 'observations'):
        if key not in daily or key not in assignment or daily[key] != assignment[key]:
            raise ValueError(f'missing or inconsistent {key}')
    digest = daily['source_sha256']
    if not isinstance(digest, str) or len(digest) != 64 or any(c not in '0123456789abcdef' for c in digest):
        raise ValueError('invalid source digest')
    if not isinstance(daily['source_bytes'], int) or daily['source_bytes'] <= 0 or not isinstance(daily['observations'], int) or daily['observations'] <= 0:
        raise ValueError('invalid counts')
    flagged = daily.get('unstable_security_membership')
    variation = assignment.get('permitted_cross_exchange_group_variation')
    conflicts = assignment.get('global_treatment_conflicts')
    local = assignment.get('within_exchange_group_changes')
    local_arm = assignment.get('within_exchange_treatment_conflicts')
    if not all(isinstance(x, list) and all(isinstance(s, str) and s for s in x) for x in (flagged, variation, conflicts, local, local_arm)):
        raise ValueError('missing or malformed conflict lists')
    if not isinstance(assignment.get('pass'), bool):
        raise ValueError('missing assignment pass status')
    if len(set(flagged)) != len(flagged) or len(set(variation)) != len(variation):
        raise ValueError('duplicate identifiers')
    permitted = sorted(set(flagged) & set(variation))
    unexplained = sorted(set(flagged) - set(permitted))
    strict_units = daily.get('strict_support_units')
    total_units = daily.get('group_exchange_units')
    if not isinstance(strict_units, int) or not isinstance(total_units, int) or total_units <= 0 or not 0 <= strict_units <= total_units:
        raise ValueError('invalid support totals')
    passed = bool(assignment['pass'] and not conflicts and not local and not local_arm and not unexplained and strict_units == total_units)
    return {'pass': passed, 'source_sha256': digest, 'source_bytes': daily['source_bytes'],
            'observations': daily['observations'], 'security_only_flags': sorted(flagged),
            'explained_cross_exchange_flags': permitted, 'unexplained_security_flags': unexplained,
            'strict_support_units': strict_units, 'group_exchange_units': total_units,
            'treatment_authenticated': False, 'historical_effect_estimated': False,
            'note': 'Diagnostic adjudication only; never substitutes for source authentication or historical inference.'}
