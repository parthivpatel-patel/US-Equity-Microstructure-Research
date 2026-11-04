"""Synthetic null rejection-size diagnostic; not market evidence."""
import numpy as np

def scan(y, window):
    x=np.arange(window,dtype=float); w=(x-x.mean())/np.sum((x-x.mean())**2)
    return np.convolve(y,w[::-1],mode='valid')[window:]-np.convolve(y,w[::-1],mode='valid')[:-window]

def indices(n,block,rng,circular):
    starts=rng.integers(0,n if circular else n-block+1,size=(n+block-1)//block)
    return np.concatenate([(s+np.arange(block))%n if circular else s+np.arange(block) for s in starts])[:n]

def trial(seed,circular,block=10,n=87,groups=9,draws=199,phi=.7,window=20):
    rng=np.random.default_rng(seed)
    common=rng.normal(size=n); independent=rng.normal(size=(groups,n))
    noise=.7*common[None,:]+.7*independent
    panel=np.zeros((groups,n))
    panel[:,0]=noise[:,0]/np.sqrt(1-phi**2)
    for t in range(1,n): panel[:,t]=phi*panel[:,t-1]+noise[:,t]
    x=np.arange(n,dtype=float); xc=x-x.mean()
    slopes=((panel-panel.mean(axis=1,keepdims=True))@xc)/(xc@xc)
    fitted=panel.mean(axis=1,keepdims=True)+slopes[:,None]*xc
    resid=panel-fitted
    observed=np.max(np.abs(scan(panel.mean(axis=0),window)))
    exceed=0
    for _ in range(draws):
        gi=rng.integers(groups,size=groups)
        ti=indices(n,block,rng,circular)
        y=(fitted[gi]+resid[gi][:,ti]).mean(axis=0)
        exceed+=np.max(np.abs(scan(y,window)))>=observed
    return (1+exceed)/(draws+1)

def experiment(reps=100):
    out={}
    for circular in (False,True):
        p=np.array([trial(153000+i,circular) for i in range(reps)])
        out['circular' if circular else 'noncircular']={'rejections_5pct':int(np.sum(p<=.05)), 'replications':reps,'mean_p':float(p.mean())}
    return out

def test():
    for c in (False,True):
        for b in (2,5,10,20):
            ix=indices(87,b,np.random.default_rng(10),c)
            assert ix.shape==(87,) and ix.min()>=0 and ix.max()<87
            if not c:
                for start in range(0,87,b):
                    assert np.all(np.diff(ix[start:start+b])==1)
    assert trial(15,False)==trial(15,False)
    result=experiment()
    assert all(0<=v['rejections_5pct']<=100 for v in result.values())
    print('PASS synthetic size calibration',result)
if __name__=='__main__': test()
