"""Exact finite-sample AR(1) contrast variance sensitivity; synthetic model only."""
import math

def variance(n, cutoff, rho):
    if not isinstance(n,int) or not isinstance(cutoff,int) or n<3 or not 0<cutoff<n or not isinstance(rho,(float,int)) or not -1<rho<1:
        raise ValueError("invalid parameters")
    w=[-1/cutoff]*cutoff+[1/(n-cutoff)]*(n-cutoff)
    return math.fsum(w[i]*w[j]*rho**abs(i-j) for i in range(n) for j in range(n))

def sensitivity(n=40,cutoffs=(10,20,30),rhos=(0,.3,.5,.8)):
    base={k:variance(n,k,0) for k in cutoffs}
    return [{"cutoff":k,"rho":rho,"variance":variance(n,k,rho),
             "iid_variance":base[k],"se_inflation":math.sqrt(variance(n,k,rho)/base[k])}
            for rho in rhos for k in cutoffs]
