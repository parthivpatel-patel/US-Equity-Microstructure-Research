"""Phase 156: independent exact reproduction and Wilson intervals for Phase 155.
Synthetic null only. Run: python tests/test_phase156_rejection_uncertainty.py
"""
import math
import numpy as np

def scan(y,w):
    if isinstance(w,bool) or not isinstance(w,(int,np.integer)) or w<2 or 2*w>len(y):
        raise ValueError("invalid window")
    x=np.arange(w,dtype=float); x-=x.mean(); weights=x/(x@x)
    s=np.convolve(y,weights[::-1],mode="valid")
    return s[w:]-s[:-w]

def block_index(n,b,rng,circular):
    starts=rng.integers(0,n if circular else n-b+1,size=(n+b-1)//b)
    return np.concatenate([((s+np.arange(b))%n if circular else s+np.arange(b)) for s in starts])[:n]

def trial(seed,phi,common_weight,block,circular,draws=99,n=87,groups=9,w=20):
    rng=np.random.default_rng(seed)
    innovations=common_weight*rng.normal(size=(1,n))+np.sqrt(1-common_weight**2)*rng.normal(size=(groups,n))
    y=np.empty((groups,n)); y[:,0]=innovations[:,0]/np.sqrt(1-phi**2)
    for t in range(1,n): y[:,t]=phi*y[:,t-1]+innovations[:,t]
    x=np.arange(n,dtype=float); xc=x-x.mean()
    slopes=((y-y.mean(axis=1,keepdims=True))@xc)/(xc@xc)
    fit=y.mean(axis=1,keepdims=True)+slopes[:,None]*xc
    resid=y-fit
    obs=np.max(np.abs(scan(y.mean(axis=0),w)))
    exceed=0
    for _ in range(draws):
        gi=rng.integers(groups,size=groups)
        ti=block_index(n,block,rng,circular)
        sim=(fit[gi]+resid[gi][:,ti]).mean(axis=0)
        exceed+=np.max(np.abs(scan(sim,w)))>=obs
    return (exceed+1)/(draws+1)

def wilson(k,n,z=1.959963984540054):
    p=k/n; d=1+z*z/n
    center=(p+z*z/(2*n))/d
    half=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d
    return center-half,center+half

def main():
    configs=[(0.,.7,10),(.7,0.,10),(.7,.7,5),(.7,.7,10),(.7,.7,20),(.9,.7,10)]
    expected=[3,0,0,0,12,12,4,8,1,0,8,9]
    observed=[]
    print("phi,common,block,method,rejections,mean_p,ci_lower,ci_upper")
    for phi,common,block in configs:
        for circ in (False,True):
            p=np.array([trial(155000+i,phi,common,block,circ) for i in range(40)])
            k=int(np.sum(p<=.05)); observed.append(k)
            lo,hi=wilson(k,40)
            print(f"{phi},{common},{block},{'circular' if circ else 'noncircular'},{k},{p.mean():.4f},{lo:.4f},{hi:.4f}")
    assert observed==expected, (observed,expected)
    tail=sum(math.comb(40,j)*.05**j*.95**(40-j) for j in range(12,41))
    print("nominal_binomial_tail_at_least_12_of_40=",format(tail,".10g"))

if __name__=="__main__": main()
