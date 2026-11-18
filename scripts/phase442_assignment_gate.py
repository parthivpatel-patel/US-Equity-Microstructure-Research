"""Reconcile global treatment with exchange-local matching; structural checks only."""
from collections import defaultdict
from datetime import date

def evaluate(rows):
    arms, local_arms, groups = defaultdict(set), defaultdict(set), defaultdict(set)
    seen = set()
    n = 0
    for line, row in enumerate(rows, 2):
        fields = ('date','security','exchange','match_group','treated')
        if any(k not in row for k in fields):
            raise ValueError(f'line {line}: missing column')
        d,s,e,g,a = (row[k].strip() if isinstance(row[k],str) else '' for k in fields)
        if not all((d,s,e,g,a)) or a not in ('0','1'):
            raise ValueError(f'line {line}: invalid identity/treatment')
        try:
            day = date.fromisoformat(d)
            if day.isoformat()!=d or day.weekday()>=5: raise ValueError()
        except ValueError as exc:
            raise ValueError(f'line {line}: invalid trading date') from exc
        if (d,s,e) in seen: raise ValueError(f'line {line}: duplicate observation')
        seen.add((d,s,e))
        arms[s].add(a); local_arms[s,e].add(a); groups[s,e].add(g)
        n+=1
    if not n: raise ValueError('empty panel')
    global_conflicts = sorted(s for s,v in arms.items() if len(v)>1)
    local_conflicts = sorted(f'{s}@{e}' for (s,e),v in local_arms.items() if len(v)>1)
    group_changes = sorted(f'{s}@{e}' for (s,e),v in groups.items() if len(v)>1)
    variation = sorted(s for s in arms if len(set().union(*(v for (security,_),v in groups.items() if security==s)))>1 and not any(key.startswith(f'{s}@') for key in group_changes))
    return {'observations':n,'global_treatment_conflicts':global_conflicts,
            'within_exchange_treatment_conflicts':local_conflicts,
            'within_exchange_group_changes':group_changes,
            'permitted_cross_exchange_group_variation':variation,
            'pass':not (global_conflicts or local_conflicts or group_changes),
            'treatment_authenticated':False,'historical_effect_estimated':False}
