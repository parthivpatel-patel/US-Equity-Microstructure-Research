"""Separate security-level treatment from exchange-level matching assignments.

Structural diagnostics only; no authenticated SEC observations or causal inference.
"""
from collections import defaultdict

def audit(rows):
    arms=defaultdict(set)
    exchange_arms=defaultdict(set)
    groups=defaultdict(set)
    security_groups=defaultdict(set)
    n=0
    for line,r in enumerate(rows,2):
        if not all(k in r for k in ('security','exchange','match_group','treated')):
            raise ValueError(f'line {line}: missing field')
        s,e,g,a=(str(r[k]).strip() if r[k] is not None else '' for k in ('security','exchange','match_group','treated'))
        if not all((s,e,g)) or a not in ('0','1'):
            raise ValueError(f'line {line}: invalid identity/arm')
        arms[s].add(a)
        exchange_arms[s,e].add(a)
        groups[s,e].add(g)
        security_groups[s].add(g)
        n+=1
    if not n: raise ValueError('empty panel')
    global_conflicts=sorted(s for s,v in arms.items() if len(v)>1)
    local_arm_conflicts=sorted(f'{s}@{e}' for (s,e),v in exchange_arms.items() if len(v)>1)
    local_group_conflicts=sorted(f'{s}@{e}' for (s,e),v in groups.items() if len(v)>1)
    cross_exchange_only=sorted(s for s,v in security_groups.items() if len(v)>1 and not any(k[0]==s and len(g)>1 for k,g in groups.items()))
    return {'observations':n,'global_treatment_conflicts':global_conflicts,
            'within_exchange_treatment_conflicts':local_arm_conflicts,
            'within_exchange_group_changes':local_group_conflicts,
            'cross_exchange_only_group_variation':cross_exchange_only,
            'structurally_eligible':not (global_conflicts or local_group_conflicts),
            'treatment_authenticated':False,'historical_effect_estimated':False}
