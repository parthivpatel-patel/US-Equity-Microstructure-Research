"""Deterministic panel composition audit; constructed examples, not SEC data."""
from math import fsum, isfinite

def audit(levels, availability, weights=None, cutoff=None):
    """Observed date-normalized and fixed-composition pre/post contrasts."""
    n = len(levels)
    if not n or len(availability) != n or not availability[0]:
        raise ValueError('invalid panel dimensions')
    T = len(availability[0]); cutoff = T//2 if cutoff is None else cutoff
    if not 1 <= cutoff < T or any(len(a) != T for a in availability):
        raise ValueError('invalid dates or cutoff')
    w = [1.0]*n if weights is None else list(weights)
    if len(w) != n or any(not isfinite(x) or x < 0 for x in w) or not fsum(w):
        raise ValueError('invalid weights')
    if any(not isfinite(v) for v in levels):
        raise ValueError('invalid levels')
    means = []
    for t in range(T):
        active = [g for g in range(n) if availability[g][t] and w[g] > 0]
        denom = fsum(w[g] for g in active)
        if not denom: raise ValueError('empty date')
        means.append(fsum(w[g]*levels[g] for g in active)/denom)
    observed = fsum(means[cutoff:])/(T-cutoff)-fsum(means[:cutoff])/cutoff
    complete = [g for g in range(n) if w[g] > 0 and all(availability[g])]
    if not complete:
        fixed = None
    else:
        fixed_mean = fsum(w[g]*levels[g] for g in complete)/fsum(w[g] for g in complete)
        fixed = fixed_mean-fixed_mean
    pre = [fsum(w[g] for g in range(n) if availability[g][t]) for t in range(cutoff)]
    post = [fsum(w[g] for g in range(n) if availability[g][t]) for t in range(cutoff,T)]
    return dict(observed_contrast=observed, complete_case_contrast=fixed,
                complete_pairs=len(complete), date_means=means,
                pre_weight_range=(min(pre),max(pre)),post_weight_range=(min(post),max(post)))

def example():
    full = [[True]*40 for _ in range(2)]
    missing = [[True]*40,[True]*20+[False]*20]
    return audit([1.,-1.],full),audit([1.,-1.],missing)

if __name__ == '__main__':
    for name,result in zip(('balanced','negative_pair_missing_post'),example()):
        print(name, {k:v for k,v in result.items() if k != 'date_means'})
