"""Exact Bartlett HAC diagnostic on date means of balanced matched-pair gaps.

Methodology only: no empirical data, causal identification or confidence intervals.
"""
from fractions import Fraction


def date_hac(rows, bandwidth):
    """Exact Bartlett long-run variance / T for balanced pair-date gaps.

    Lag indexes observed trading sessions. Captures serial dependence in date
    averages, not arbitrary pair-cluster dependence or selection bias.
    """
    from datetime import date
    rows = tuple(rows)
    if not rows:
        raise ValueError('empty panel')
    cells, pairs, dates = {}, set(), set()
    for row in rows:
        if len(row) != 3:
            raise ValueError('expected pair/date/gap')
        p, d, x = row
        if not isinstance(p, str) or not p or not isinstance(d, str):
            raise ValueError('invalid pair/date')
        try:
            if date.fromisoformat(d).isoformat() != d:
                raise ValueError('noncanonical date')
        except (TypeError, ValueError) as exc:
            raise ValueError('invalid ISO date') from exc
        if type(x) not in (int, Fraction):
            raise ValueError('gap must be exact rational')
        if (p, d) in cells:
            raise ValueError('duplicate cell')
        cells[p, d] = Fraction(x)
        pairs.add(p)
        dates.add(d)
    t = len(dates)
    if len(pairs) < 2 or t < 3 or len(cells) != len(pairs)*t:
        raise ValueError('requires balanced panel with >=2 pairs and >=3 dates')
    if type(bandwidth) is not int or not 0 <= bandwidth < t:
        raise ValueError('bandwidth must be integer in [0,T)')
    ordered = sorted(dates)
    means = [sum((cells[p,d] for p in pairs), Fraction())/len(pairs) for d in ordered]
    mu = sum(means, Fraction())/t
    u = [x-mu for x in means]
    gamma = [sum((u[i]*u[i-lag] for i in range(lag,t)), Fraction())/t for lag in range(bandwidth+1)]
    long_run = gamma[0] + 2*sum((Fraction(bandwidth+1-lag,bandwidth+1)*gamma[lag] for lag in range(1,bandwidth+1)), Fraction())
    return {'mean':mu, 'variance_of_mean':long_run/t, 'long_run_variance':long_run,
            'autocovariances':tuple(gamma), 'n_pairs':len(pairs), 'n_dates':t,
            'bandwidth':bandwidth, 'causal_identification_established':False}
