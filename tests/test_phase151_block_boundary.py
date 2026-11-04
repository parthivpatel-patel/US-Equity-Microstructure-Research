"""Phase 151: synthetic-only block seam and shared-date diagnostic."""
import numpy as np

def sample_indices(n, block, seed, circular):
    if not isinstance(n,int) or not isinstance(block,int) or n<2 or not 1<=block<=n:
        raise ValueError("invalid n/block")
    rng=np.random.default_rng(seed)
    starts=rng.integers(0,n if circular else n-block+1,size=(n+block-1)//block)
    return np.concatenate([((s+np.arange(block))%n if circular else s+np.arange(block)) for s in starts])[:n]

def diagnostics(series, ix, block):
    series=np.asarray(series,dtype=float); ix=np.asarray(ix,dtype=int)
    if series.ndim!=1 or len(series)!=len(ix) or not np.isfinite(series).all() or np.any(ix<0) or np.any(ix>=len(series)):
        raise ValueError("invalid data")
    differences=np.abs(np.diff(series[ix]))
    mask=np.zeros(len(differences),dtype=bool)
    mask[np.arange(block-1,len(series)-1,block)]=True
    return (float(differences[mask].mean()) if mask.any() else float("nan"),
            float(differences[~mask].mean()) if (~mask).any() else float("nan"),
            int(mask.sum()),int((~mask).sum()))

def test():
    n=87; block=10; x=np.arange(n)
    series=np.sin(x/7)+0.2*np.cos(x/3)
    for circular in (False,True):
        for seed in range(200):
            ix=sample_indices(n,block,seed,circular)
            assert len(ix)==n
            for start in range(0,n,block):
                d=np.diff(ix[start:start+block])
                assert np.all((d==1)|(d==-(n-1))) if circular else np.all(d==1)
            assert diagnostics(series,ix,block)[2:]==(8,78)
    assert diagnostics(np.arange(10,dtype=float),np.array([0,1,2,3,4,0,1,2,3,4]),5)==(4.,1.,1,8)
    common=np.sin(x/7)
    panel=np.stack([common+0.1*i for i in range(9)])
    ix=sample_indices(n,block,151,False)
    np.testing.assert_allclose(panel[:,ix]-panel[0,ix],np.broadcast_to(np.arange(9)[:,None]*0.1,(9,n)),atol=1e-14)
    for bad in (0,-1,88):
        try: sample_indices(n,bad,0,False)
        except ValueError: pass
        else: raise AssertionError("invalid block accepted")
    print("PASS: 400 seeded index trials; seam control; shared-date control; invalid blocks")

if __name__=="__main__": test()
