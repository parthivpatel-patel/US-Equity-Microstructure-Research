"""Synthetic sensitivity audit of Phase 153; not SEC observations."""
import numpy as np

def scan(y,w):
    if w<2 or 2*w>len(y): raise ValueError('invalid window')
    x=np.arange(w,dtype=float); x-=x.mean(); weights=x/(x@x)
    s=np.convolve(y,weights[::-1],mode='valid')
    return s[w:]-s[:-w]

def block_index(n,b,rng,circular):
    starts=rng.integers(0,n if circular else n-b+1,size=(n+b-1)//b)
    return np.concatenate([((s+np.arange(b))%n if circular else s+np.arange(b)) for s in starts])[:n]

def trial(seed,phi,common_weight,block,circular,draws=99,n=87,groups=9,w=20):
    rng=np.random.default_rng(seed)
    innovations=common_weight*rng.normal(size=(1,n))+np.sqrt(1-common_weight**2)*rng.normal(size=(groups,n))
    y=np.empty((groups,n)); y[:,0]=innovations[:,0]/np.sqrt(1-phi**2)
    for t in range(1,n):y[:,t]=phi*y[:,t-1]+innovations[:,t]
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

def experiment(reps=40):
    results=[]
    for phi,common,block in [(0.0,0.7,10),(0.7,0.0,10),(0.7,0.7,5),(0.7,0.7,10),(0.7,0.7,20),(0.9,0.7,10)]:
        for circular in (False,True):
            p=np.array([trial(155000+i,phi,common,block,circular) for i in range(reps)])
            results.append((phi,common,block,'circular' if circular else 'noncircular',int(np.sum(p<=.05)),round(float(p.mean()),4)))
    return results

def test():
    assert scan(np.arange(10.),2).shape==(7,)
    assert np.allclose(scan(np.arange(10.),2),0)
    assert trial(4,.7,.7,10,False)==trial(4,.7,.7,10,False)
    for r in experiment():print(','.join(map(str,r)))
if __name__=='__main__':test()
