"""Phase 150: synthetic-only noncircular common-calendar moving-block diagnostic."""
import numpy as np

def indices(dates, block, rng, circular=False):
    if not isinstance(dates,int) or not isinstance(block,int) or dates<2 or not 1<=block<=dates:
        raise ValueError("invalid dates/block")
    starts=rng.integers(0,dates if circular else dates-block+1,size=(dates+block-1)//block)
    return np.concatenate([((s+np.arange(block))%dates if circular else np.arange(s,s+block)) for s in starts])[:dates]

def test():
    for t in (40,87,106):
        for b in (2,5,10,20):
            for seed in range(50):
                ix=indices(t,b,np.random.default_rng(seed))
                assert ix.shape==(t,) and ix.min()>=0 and ix.max()<t
                for k in range(0,t,b):
                    np.testing.assert_array_equal(np.diff(ix[k:k+b]),np.ones(len(ix[k:k+b])-1,dtype=int))
    t=87; x=np.arange(t); common=np.sin(x/7)
    panel=np.stack([common+i*.1 for i in range(9)])
    ix=indices(t,7,np.random.default_rng(150))
    np.testing.assert_allclose(panel[:,ix]-panel[0,ix],np.broadcast_to(np.arange(9)[:,None]*.1,(9,t)),atol=1e-14)
    circ_wrap=mov_wrap=0
    for seed in range(100):
        a=indices(87,10,np.random.default_rng(seed),True)
        b=indices(87,10,np.random.default_rng(seed))
        circ_wrap+=sum(np.any(np.diff(a[k:k+10])<0) for k in range(0,87,10))
        mov_wrap+=sum(np.any(np.diff(b[k:k+10])<0) for k in range(0,87,10))
    assert circ_wrap==95 and mov_wrap==0
    print("PASS: 600 index tests, shared calendar shock; circular wraps",circ_wrap,"noncircular wraps",mov_wrap)

if __name__=="__main__": test()
