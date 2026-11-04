"""Phase 152: synthetic AR(1) block-seam calibration; not SEC evidence."""
import numpy as np

def sample_indices(n, block, rng, circular):
    if not isinstance(n,int) or not isinstance(block,int) or n<3 or not 2<=block<=n:
        raise ValueError("invalid dimensions")
    starts=rng.integers(0,n if circular else n-block+1,size=(n+block-1)//block)
    return np.concatenate([((s+np.arange(block))%n if circular else s+np.arange(block)) for s in starts])[:n]

def boundary_metrics(values, indices, block):
    x=np.asarray(values,float); ix=np.asarray(indices,int)
    if x.ndim!=1 or ix.shape!=x.shape or not np.isfinite(x).all() or np.any(ix<0) or np.any(ix>=len(x)):
        raise ValueError("invalid data")
    jumps=np.abs(np.diff(x[ix])); seam=np.zeros(len(jumps),bool)
    seam[np.arange(block-1,len(jumps),block)]=True
    if not seam.any() or not (~seam).any(): raise ValueError("need seam and interior")
    return float(jumps[seam].mean()),float(jumps[~seam].mean())

def experiment(reps=1000,seed=152,n=87,block=10):
    rng=np.random.default_rng(seed)
    shocks=rng.normal(size=n); x=np.empty(n)
    x[0]=shocks[0]/np.sqrt(1-0.7**2)
    for t in range(1,n): x[t]=0.7*x[t-1]+shocks[t]
    out={}
    for circular in (False,True):
        ratios=[]; diffs=[]; wraps=0
        for _ in range(reps):
            ix=sample_indices(n,block,rng,circular)
            seam,interior=boundary_metrics(x,ix,block)
            ratios.append(seam/interior); diffs.append(seam-interior)
            wraps+=sum(np.any(np.diff(ix[k:k+block])<0) for k in range(0,n,block))
        out["circular" if circular else "noncircular"]={
            "mean_ratio":float(np.mean(ratios)),
            "mean_difference":float(np.mean(diffs)),
            "within_block_wraps":int(wraps)}
    return out

def test():
    assert experiment()==experiment()
    assert sample_indices(87,10,np.random.default_rng(0),False).shape==(87,)
    assert boundary_metrics(np.arange(10),np.array([0,1,2,3,4,0,1,2,3,4]),5)==(4.,1.)
    for b in (0,1,88):
        try: sample_indices(87,b,np.random.default_rng(0),False)
        except ValueError: pass
        else: raise AssertionError("bad block accepted")
    result=experiment()
    assert result["noncircular"]["within_block_wraps"]==0
    assert result["circular"]["within_block_wraps"]>0
    assert all(np.isfinite(v["mean_ratio"]) for v in result.values())
    print("PASS deterministic synthetic seam diagnostic",result)

if __name__=="__main__": test()
