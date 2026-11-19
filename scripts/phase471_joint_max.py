"""Analytical Gaussian simultaneous placebo benchmark; NOT historical SEC inference."""
import numpy as np
from scipy.stats import norm

def ar1_correlation(n=40, splits=(10, 20, 30), rho=0.5):
    if not isinstance(n,int) or n<3 or not -1<rho<1 or len(set(splits))!=len(splits) or not all(isinstance(k,int) and 0<k<n for k in splits):
        raise ValueError("invalid design")
    t=np.arange(n)
    sigma=rho**np.abs(t[:,None]-t[None,:])
    w=np.array([[-1/k if i<k else 1/(n-k) for i in range(n)] for k in splits])
    cov=w@sigma@w.T
    std=np.sqrt(np.diag(cov))
    return cov/std[:,None]/std[None,:]

def calibrate(rho=0.5,draws=200000,seed=471):
    """Seeded Monte Carlo benchmark; not exact probability or empirical test."""
    if not isinstance(draws,int) or draws<1000: raise ValueError("draws too small")
    r=ar1_correlation(rho=rho)
    rng=np.random.default_rng(seed)
    z=rng.standard_normal((draws,len(r)))@np.linalg.cholesky(r).T
    mx=np.max(np.abs(z),axis=1)
    return {"rho":rho,"joint_critical":float(np.quantile(mx,.95)),
      "naive_familywise":float(np.mean(mx>norm.ppf(.975))),
      "bonferroni_familywise":float(np.mean(mx>norm.ppf(1-.05/(2*len(r))))),
      "bonferroni_critical":float(norm.ppf(1-.05/(2*len(r)))),"draws":draws}

if __name__=="__main__":
    for rho in (0,.3,.5,.8): print(calibrate(rho=rho))
