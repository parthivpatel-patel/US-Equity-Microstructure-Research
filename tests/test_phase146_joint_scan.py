"""Phase 146: joint group/common-calendar block scan mechanics; synthetic tests only."""
import numpy as np

def scan(y, window=20):
    y=np.asarray(y,dtype=float)
    if y.ndim!=1 or len(y)<2*window or not np.isfinite(y).all():
        raise ValueError("invalid series")
    x=np.arange(window,dtype=float)
    w=(x-x.mean())/np.sum((x-x.mean())**2)
    s=np.convolve(y,w[::-1],mode="valid")
    return s[window:]-s[:-window]

def joint_indices(groups,dates,block,rng):
    if groups<1 or dates<2 or not 1<=block<=dates:
        raise ValueError("invalid dimensions")
    gi=rng.integers(groups,size=groups)
    starts=rng.integers(dates,size=(dates+block-1)//block)
    ti=np.concatenate([(s+np.arange(block))%dates for s in starts])[:dates]
    return gi,ti

def simulate(panel,block=5,draws=100,seed=146,window=20):
    panel=np.asarray(panel,dtype=float)
    if panel.ndim!=2 or not np.isfinite(panel).all() or panel.shape[1]<2*window or draws<1:
        raise ValueError("invalid panel")
    rng=np.random.default_rng(seed)
    n,t=panel.shape
    x=np.arange(t,dtype=float); xc=x-x.mean()
    slopes=((panel-panel.mean(axis=1,keepdims=True))@xc)/(xc@xc)
    fitted=panel.mean(axis=1,keepdims=True)+slopes[:,None]*xc
    resid=panel-fitted
    observed=float(np.max(np.abs(scan(panel.mean(axis=0),window))))
    maxima=[]
    for _ in range(draws):
        gi,ti=joint_indices(n,t,block,rng)
        y=(fitted[gi]+resid[gi][:,ti]).mean(axis=0)
        maxima.append(float(np.max(np.abs(scan(y,window)))))
    maxima=np.asarray(maxima)
    return observed,maxima,(1+np.count_nonzero(maxima>=observed))/(draws+1)

def test():
    rng=np.random.default_rng(146)
    gi,ti=joint_indices(7,87,5,rng)
    assert gi.shape==(7,) and ti.shape==(87,)
    for k in range(0,85,5):
        np.testing.assert_array_equal(ti[k:min(k+5,87)],(ti[k]+np.arange(min(5,87-k)))%87)
    x=np.arange(87,dtype=float)
    panel=np.array([2*i+.3*x for i in range(7)])
    observed,null,p=simulate(panel,draws=100)
    assert abs(observed)<1e-12 and np.max(abs(null))<1e-12
    panel2=panel.copy()
    panel2[:,45:]+=np.arange(42)*.6
    obs2,null2,p2=simulate(panel2,draws=100)
    assert obs2>0 and len(null2)==100 and 1/101<=p2<=1
    a=simulate(panel2,draws=100,seed=55)
    b=simulate(panel2,draws=100,seed=55)
    np.testing.assert_array_equal(a[1],b[1])
    assert a[2]==b[2]
    for bad in [np.zeros((2,10)),np.array([[np.nan]*87])]:
        try: simulate(bad)
        except ValueError: pass
        else: raise AssertionError("invalid panel accepted")
    print("PASS: joint-index mechanics, synthetic break, deterministic bootstrap and validation")

if __name__=="__main__": test()
