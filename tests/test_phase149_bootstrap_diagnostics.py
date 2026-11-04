"""Phase 149: synthetic-only diagnostics for Phase 146 whole-scan bootstrap."""
import numpy as np

def scan(y, window=20):
    y=np.asarray(y,dtype=float)
    if y.ndim!=1 or len(y)<2*window or not np.isfinite(y).all():
        raise ValueError('invalid series')
    x=np.arange(window,dtype=float)
    w=(x-x.mean())/np.sum((x-x.mean())**2)
    s=np.convolve(y,w[::-1],mode='valid')
    return s[window:]-s[:-window]

def diagnostics():
    t=87; w=20; x=np.arange(t,dtype=float)
    # Deterministic counterexample: residual sequence with endpoint discontinuity.
    r=np.sin(2*np.pi*x/29)+0.04*x
    r=r-(r.mean()+np.dot(x-x.mean(),r-r.mean())/np.dot(x-x.mean(),x-x.mean())*(x-x.mean()))
    assert abs(r.mean())<1e-12 and abs(np.dot(x-x.mean(),r))<1e-10
    # Circular resampling wraps the last residual directly to the first.
    seam=abs(r[-1]-r[0]); adjacent=np.abs(np.diff(r))
    print('residual endpoint jump',round(seam,9),'maximum ordinary adjacent jump',round(adjacent.max(),9))
    assert seam>adjacent.max()
    # A common calendar draw preserves contemporaneous group co-movement.
    rng=np.random.default_rng(149)
    common=np.sin(x/5)
    panel=np.vstack([common+0.01*i*np.cos(x/7) for i in range(8)])
    starts=rng.integers(t,size=(t+4)//5)
    idx=np.concatenate([(s+np.arange(5))%t for s in starts])[:t]
    resampled=panel[:,idx]
    assert np.allclose(resampled[1]-resampled[0],0.01*np.cos(x[idx]/7))
    # Independent group draws can over-represent groups; this is expected, not a bug.
    groups=rng.integers(8,size=8)
    assert len(groups)==8
    print('candidate breakpoints',len(scan(common,w)))
    assert len(scan(common,w))==48
    print('PASS: circular seam counterexample, shared calendar indexing, 48 candidate dates')

if __name__=='__main__': diagnostics()
