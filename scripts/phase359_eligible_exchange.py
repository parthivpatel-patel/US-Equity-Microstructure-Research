"""Exchange support sensitivity. Eligibility must be authenticated externally."""
from collections import defaultdict
from math import fsum, isfinite

STATUSES = {'observed','source_missing','not_listed','not_trading','exchange_not_applicable'}

def compare_exchange_support(rows, exchanges, eligible_by_security_date):
    exchanges = tuple(exchanges)
    if not exchanges or len(set(exchanges)) != len(exchanges) or any(not isinstance(e,str) or not e.strip() for e in exchanges):
        raise ValueError('invalid exchange universe')
    if not isinstance(eligible_by_security_date,dict) or not eligible_by_security_date:
        raise ValueError('explicit eligibility policy required')
    policy={}
    for key, eligible in eligible_by_security_date.items():
        if not isinstance(key,tuple) or len(key)!=2 or any(not isinstance(k,str) or not k.strip() for k in key):
            raise ValueError('invalid policy key')
        eligible=tuple(eligible)
        if not eligible or len(set(eligible))!=len(eligible) or not set(eligible).issubset(exchanges):
            raise ValueError('invalid eligible set')
        policy[key]=set(eligible)
    cells=defaultdict(dict)
    for security,day,exchange,status,value in rows:
        key=(security,day)
        if key not in policy or exchange not in exchanges or exchange in cells[key] or status not in STATUSES:
            raise ValueError('unexpected duplicate or invalid cell')
        if status=='observed':
            if isinstance(value,bool) or not isinstance(value,(int,float)) or not isfinite(value) or value<0:
                raise ValueError('invalid metric')
        elif value is not None:
            raise ValueError('nonobserved value must be None')
        cells[key][exchange]=(status,value)
    if set(cells)!=set(policy):
        raise ValueError('missing security-date rows')
    strict,eligible_totals,excluded={},{},{}
    for key in sorted(policy):
        if set(cells[key])!=set(exchanges):
            raise ValueError('incomplete exchange grid')
        eligible=policy[key]
        for e in exchanges:
            if e not in eligible and cells[key][e][0]!='exchange_not_applicable':
                raise ValueError('excluded exchange not explicitly inapplicable')
            if e in eligible and cells[key][e][0]=='exchange_not_applicable':
                raise ValueError('eligible exchange marked inapplicable')
        unavailable=sorted(e for e in eligible if cells[key][e][0]!='observed')
        if unavailable:
            excluded[key]={'unobserved_eligible_exchanges':unavailable}
            continue
        total=fsum(cells[key][e][1] for e in eligible)
        if not isfinite(total):
            raise ValueError('nonfinite aggregate')
        eligible_totals[key]=total
        if eligible==set(exchanges):
            strict[key]=total
    return {'strict_complete_universe':strict,'declared_eligible':eligible_totals,
            'excluded':excluded,'strict_n':len(strict),'eligible_n':len(eligible_totals),
            'policy_authenticated':False,'status':'DESCRIPTIVE_POLICY_UNAUTHENTICATED_NO_CAUSAL_CLAIM'}
