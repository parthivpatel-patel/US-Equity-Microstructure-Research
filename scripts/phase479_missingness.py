"""Exact covariance of a weighted panel pre/post contrast with missing cells.
Constructed model only; not historical SEC observations. Standard library.
"""
from math import fsum, sqrt

def contrast_variance(loadings, availability, pair_weights=None, rho_factor=0.5, rho_residual=0.5, residual_variance=2.0):
    n=len(loadings)
    if not n or len(availability)!=n or not availability[0]: raise ValueError('empty or mismatched panel')
    T=len(availability[0]); half=T//2
    if T<4 or T%2 or any(len(row)!=T for row in availability): raise ValueError('invalid dates')
    if not (-1<rho_factor<1 and -1<rho_residual<1) or residual_variance<=0: raise ValueError('invalid covariance')
    weights=[1.0]*n if pair_weights is None else pair_weights
    if len(weights)!=n or any(w<0 for w in weights) or fsum(weights)<=0: raise ValueError('invalid weights')
    coeff=[[0.0]*T for _ in range(n)]
    for t in range(T):
        denom=fsum(weights[g] for g in range(n) if availability[g][t])
        if denom<=0: raise ValueError('date without positive-weight observations')
        sign=(-1 if t<half else 1)/half
        for g in range(n):
            if availability[g][t]: coeff[g][t]=sign*weights[g]/denom
    b=[fsum(coeff[g][t]*loadings[g] for g in range(n)) for t in range(T)]
    factor=fsum(b[t]*b[s]*rho_factor**abs(t-s) for t in range(T) for s in range(T))
    residual=residual_variance*fsum(coeff[g][t]*coeff[g][s]*rho_residual**abs(t-s) for g in range(n) for t in range(T) for s in range(T))
    return {'factor_variance':factor,'residual_variance':residual,'total_variance':factor+residual,'se_inflation':sqrt((factor+residual)/residual),'date_exposures':b,'coefficients':coeff}

def example():
    load=[.5,-.5]; full=[[True]*40 for _ in load]
    missing=[[True]*40,[True]*20+[False]*20]
    return contrast_variance(load,full),contrast_variance(load,missing)

if __name__=='__main__':
    a,b=example()
    for name,r in [('balanced',a),('post_missing_negative',b)]:
        print(name, {k:round(r[k],10) for k in ('factor_variance','residual_variance','total_variance','se_inflation')})
