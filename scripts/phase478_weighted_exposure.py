"""Exact weighted factor covariance benchmark; synthetic only; standard library."""
from math import sqrt, fsum

def variance_components(loadings, weights, rho_factor=0.5, rho_residual=0.5, n_dates=40, residual_variance=2.0):
    if len(loadings)!=len(weights) or not loadings or any(x<0 for x in weights) or sum(weights)<=0:
        raise ValueError('invalid pair weights')
    if not (-1<rho_factor<1 and -1<rho_residual<1) or n_dates%2 or n_dates<4:
        raise ValueError('invalid AR(1) or date count')
    z=fsum(weights); p=[v/z for v in weights]; half=n_dates//2
    t=[-1/half]*half+[1/half]*half
    def q(r):
        return fsum(t[i]*t[j]*r**abs(i-j) for i in range(n_dates) for j in range(n_dates))
    mean_loading=fsum(a*b for a,b in zip(p,loadings))
    residual=residual_variance*fsum(v*v for v in p)*q(rho_residual)
    factor=mean_loading**2*q(rho_factor)
    return dict(mean_loading=mean_loading,effective_pairs=1/fsum(v*v for v in p),residual_variance=residual,factor_variance=factor,se_inflation=sqrt((residual+factor)/residual))

if __name__=='__main__':
    patterns={'equal':([.5]*34+[-.5]*34,[1]*68), 'positive_double':([.5]*34+[-.5]*34,[2]*34+[1]*34), 'negative_double':([.5]*34+[-.5]*34,[1]*34+[2]*34), 'positive_quadruple':([.5]*34+[-.5]*34,[4]*34+[1]*34)}
    for name,(loadings,weights) in patterns.items():
        print(name,variance_components(loadings,weights))
