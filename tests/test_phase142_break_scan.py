"""Independent synthetic-data regression tests for Phase 141 breakpoint indexing.
No historical market observations are embedded or simulated as empirical evidence.
"""
import numpy as np

def scan(y, window=20):
    y=np.asarray(y,dtype=float)
    x=np.arange(window,dtype=float)
    x=x-x.mean()
    denom=np.dot(x,x)
    out=[]
    for i in range(window,len(y)-window+1):
        left=np.dot(x,y[i-window:i])/denom
        right=np.dot(x,y[i:i+window])/denom
        out.append((i,right-left))
    return out

def test_constant_linear():
    assert max(abs(v) for _,v in scan(np.ones(87)))<1e-12
    assert max(abs(v) for _,v in scan(np.arange(87)*2.5+7))<1e-12

def test_piecewise():
    t=np.arange(87)
    y=np.where(t<44,2*t,88-3*(t-44))
    vals=dict(scan(y))
    assert abs(vals[44]+5)<1e-12
    assert len(vals)==48

def test_shift_invariance():
    y=np.sin(np.arange(87)/5)
    a=scan(y)
    b=scan(y+1e5)
    assert np.allclose([v for _,v in a],[v for _,v in b],atol=1e-10)

if __name__=='__main__':
    test_constant_linear();test_piecewise();test_shift_invariance()
    print('PASS: 4 deterministic checks; 48 candidate indices for 87 dates')
