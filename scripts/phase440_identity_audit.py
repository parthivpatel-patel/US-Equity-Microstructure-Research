"""Cross-exchange identity diagnostic for matched panels; no historical estimation."""
from collections import defaultdict

def audit(rows):
    by_security = defaultdict(set)
    by_security_exchange = defaultdict(set)
    count = 0
    for row in rows:
        s, e, g, a = (str(row[k]).strip() for k in ('security','exchange','match_group','treated'))
        if not all((s,e,g)) or a not in ('0','1'):
            raise ValueError('invalid identity or assignment')
        by_security[s].add((g,a,e))
        by_security_exchange[(s,e)].add((g,a))
        count += 1
    if not count:
        raise ValueError('empty panel')
    unstable = sorted(f'{s}@{e}' for (s,e), assignments in by_security_exchange.items() if len(assignments)>1)
    cross_exchange = sorted(s for s, assignments in by_security.items() if len({e for _,_,e in assignments})>1)
    return {'observations':count,'unstable_security_exchange_assignments':unstable,
            'securities_on_multiple_exchanges':cross_exchange,
            'identity_scope':'security+exchange', 'historical_effect_estimated':False,
            'source_authenticated':False}
