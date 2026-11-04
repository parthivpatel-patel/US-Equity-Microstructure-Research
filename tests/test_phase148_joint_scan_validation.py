"""Phase 148 fail-closed wrapper for Phase 146 joint-scan mechanics; synthetic only."""
import numpy as np
from test_phase146_joint_scan import scan, simulate

def checked_scan(y, window=20):
    a=np.asarray(y,dtype=float)
    if (a.ndim!=1 or isinstance(window,(bool,np.bool_))
        or not isinstance(window,(int,np.integer)) or window<2
        or len(a)<2*window or not np.isfinite(a).all()):
        raise ValueError("invalid scan inputs")
    out=scan(a,window)
    if len(out)!=len(a)-2*window+1 or not np.isfinite(out).all():
        raise ValueError("invalid scan output")
    return out

def checked_simulate(panel,block=5,draws=100,seed=148,window=20):
    a=np.asarray(panel,dtype=float)
    ints=(block,draws,window,seed)
    if (a.ndim!=2 or a.shape[0]<2 or not np.isfinite(a).all()
        or any(isinstance(v,(bool,np.bool_)) or not isinstance(v,(int,np.integer)) for v in ints)
        or window<2 or a.shape[1]<2*window or not 1<=block<=a.shape[1]
        or draws<1 or seed<0):
        raise ValueError("invalid bootstrap inputs")
    obs,null,p=simulate(a,block=block,draws=draws,seed=seed,window=window)
    if not np.isfinite(obs) or null.shape!=(draws,) or not np.isfinite(null).all() or not 0<p<=1:
        raise ValueError("invalid bootstrap output")
    return obs,null,p

def test():
    x=np.arange(87,dtype=float)
    panel=np.stack([i+.02*i*x+np.sin(x/6+i) for i in range(2,11)])
    for w in (2,3,5,10,20):
        np.testing.assert_array_equal(checked_scan(panel[0],w),scan(panel[0],w))
    a=checked_simulate(panel,draws=40)
    b=simulate(panel,block=5,draws=40,seed=148,window=20)
    assert a[0]==b[0] and a[2]==b[2]
    np.testing.assert_array_equal(a[1],b[1])
    invalid=0
    for w in (0,1,-1,1.5,True,44):
        try: checked_scan(panel[0],w)
        except ValueError: invalid+=1
        else: raise AssertionError("invalid window accepted")
    for overrides in ({"window":1},{"window":0},{"window":44},{"block":0},
                      {"block":88},{"draws":0},{"draws":1.5},{"block":True},{"seed":-1}):
        kwargs=dict(block=5,draws=10,seed=148,window=20)
        kwargs.update(overrides)
        try: checked_simulate(panel,**kwargs)
        except ValueError: invalid+=1
        else: raise AssertionError("invalid bootstrap argument accepted")
    for bad in (panel[:1],np.full((3,87),np.nan),np.zeros((2,39))):
        try: checked_simulate(bad,draws=10)
        except ValueError: invalid+=1
        else: raise AssertionError("invalid panel accepted")
    print("PASS: 18 invalid cases, five scan equivalence cases, bootstrap equivalence")

if __name__=="__main__": test()
