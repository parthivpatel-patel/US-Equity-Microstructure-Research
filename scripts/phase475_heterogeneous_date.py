"""Exact covariance of matched treated-control placebo contrasts under AR(1) common dates."""
from math import sqrt

def weights(n, cutoff):
    if not isinstance(n,int) or not isinstance(cutoff,int) or not 0 < cutoff < n: raise ValueError('invalid cutoff')
    return [-1/cutoff if t < cutoff else 1/(n-cutoff) for t in range(n)]

def covariance(n, cutoffs, groups, date_variance, idio_variance, rho, loading_difference):
    if groups < 1 or date_variance < 0 or idio_variance < 0 or abs(rho)>=1: raise ValueError('invalid parameters')
    ws=[weights(n,k) for k in cutoffs]
    out=[]
    for a in ws:
        row=[]
        for b in ws:
            common=sum(a[t]*b[s]*rho**abs(t-s) for t in range(n) for s in range(n))*date_variance*loading_difference**2
            idio=2*idio_variance/groups*sum(x*y for x,y in zip(a,b))
            row.append(common+idio)
        out.append(row)
    return out

def benchmark():
    for delta in (0,0.1,0.5,1):
        for rho in (0,0.5):
            v=covariance(40,[10,20,30],68,1,1,rho,delta)
            baseline=covariance(40,[10,20,30],68,0,1,rho,delta)
            print(f'delta={delta:.1f} rho={rho:.1f} variance_middle={v[1][1]:.9f} SE_inflation={sqrt(v[1][1]/baseline[1][1]):.6f}')
if __name__=='__main__': benchmark()
