"""Independent assignment-scope regression; no SEC data or causal estimates."""
from collections import defaultdict

def compare_scopes(rows):
    """Compare security-only versus security/exchange matching-conflict flags."""
    global_groups, local_groups, treatment = defaultdict(set), defaultdict(set), defaultdict(set)
    n = 0
    for row in rows:
        s, e, g, t = (row[k] for k in ('security', 'exchange', 'match_group', 'treated'))
        if not all(isinstance(v, str) and v.strip() for v in (s, e, g, t)) or t not in ('0', '1'):
            raise ValueError('invalid assignment row')
        global_groups[s].add(g)
        local_groups[s, e].add(g)
        treatment[s].add(t)
        n += 1
    if n == 0:
        raise ValueError('empty rows')
    false_positive = sorted(s for s, groups in global_groups.items()
                            if len(groups) > 1 and all(len(local_groups[s, e]) == 1
                            for ss, e in local_groups if ss == s))
    return {
        'observations': n,
        'security_only_matching_conflicts': sorted(s for s, v in global_groups.items() if len(v) > 1),
        'within_exchange_matching_conflicts': sorted(f'{s}@{e}' for (s, e), v in local_groups.items() if len(v) > 1),
        'false_positive_security_only_matching_flags': false_positive,
        'global_treatment_conflicts': sorted(s for s, v in treatment.items() if len(v) > 1),
        'historical_effect_estimated': False,
    }
