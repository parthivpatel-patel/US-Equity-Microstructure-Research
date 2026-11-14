"""Strict source-coverage audit; does not infer missing records are zero trades."""
from collections import Counter
from datetime import date

STATUSES = frozenset({'observed','source_missing','not_listed','not_trading','exchange_not_applicable'})

def audit_coverage(rows, sessions, securities, exchanges):
    """Rows: (security, session, exchange, status, value); complete declared grid required.

    Values are permitted only for observed cells; observed zero is distinct from missing.
    Returns count summaries, never imputes a missing value or infers eligibility.
    """
    def unique_strings(values, name):
        v = list(values)
        if not v or any(not isinstance(x,str) or not x.strip() for x in v) or len(v)!=len(set(v)):
            raise ValueError('invalid '+name)
        return v
    sessions=unique_strings(sessions,'sessions')
    try:
        if any(date.fromisoformat(s).isoformat()!=s for s in sessions): raise ValueError('invalid sessions')
    except (TypeError,ValueError) as exc: raise ValueError('invalid sessions') from exc
    if sessions != sorted(sessions): raise ValueError('unsorted sessions')
    securities=unique_strings(securities,'securities')
    exchanges=unique_strings(exchanges,'exchanges')
    expected={(s,d,e) for s in securities for d in sessions for e in exchanges}
    seen={}; counts=Counter(); observed_zero=0
    for security,session,exchange,status,value in rows:
        key=(security,session,exchange)
        if key not in expected: raise ValueError('out-of-universe cell')
        if key in seen: raise ValueError('duplicate cell')
        if status not in STATUSES: raise ValueError('invalid status')
        if status=='observed':
            if isinstance(value,bool) or not isinstance(value,(int,float)) or not __import__('math').isfinite(value) or value<0:
                raise ValueError('invalid observed nonnegative metric')
            observed_zero += value==0
        elif value is not None: raise ValueError('non-observed cell has value')
        seen[key]=status; counts[status]+=1
    absent=expected-seen.keys()
    if absent: raise ValueError('undeclared cells: '+str(len(absent)))
    return {'cells':len(expected),'status_counts':{s:counts[s] for s in sorted(STATUSES)},
            'observed_zero_cells':observed_zero,'observed_positive_cells':counts['observed']-observed_zero,
            'fully_observed_security_dates':sum(all(seen[(s,d,e)]=='observed' for e in exchanges) for s in securities for d in sessions),
            'status':'COVERAGE_ONLY_NO_IMPUTATION_NO_CAUSAL_CLAIM'}
