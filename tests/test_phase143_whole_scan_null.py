"""Phase 143: exploratory whole-scan null calibration; synthetic tests only."""
import numpy as np

def slopes(y, window=20):
    y = np.asarray(y, dtype=float)
    if y.ndim != 1 or len(y) < 2*window or not np.isfinite(y).all():
        raise ValueError("finite 1D series with at least 2*window observations required")
    x = np.arange(window, dtype=float)
    weights = (x-x.mean()) / np.sum((x-x.mean())**2)
    before = np.convolve(y, weights[::-1], mode="valid")
    return before[window:] - before[:-window]

def max_stat(y, window=20):
    return float(np.max(np.abs(slopes(y, window))))

def circular_block_indices(n, block, rng):
    if not 1 <= block <= n:
        raise ValueError("block length outside 1..n")
    starts = rng.integers(0, n, size=(n+block-1)//block)
    return np.concatenate([(start+np.arange(block)) % n for start in starts])[:n]

def null_maxima(y, block=5, draws=100, seed=143, window=20):
    """Exploratory linear-null residual bootstrap; requires null/stationarity validation."""
    y = np.asarray(y, dtype=float)
    max_stat(y, window)
    x = np.arange(len(y), dtype=float)
    coef = np.polyfit(x, y, 1)
    fit = np.polyval(coef, x)
    resid = y-fit
    resid -= resid.mean()
    rng = np.random.default_rng(seed)
    return np.array([max_stat(fit+resid[circular_block_indices(len(y),block,rng)],window)
                     for _ in range(draws)])

def test():
    x = np.arange(87, dtype=float)
    assert len(slopes(x,20)) == 48
    assert np.allclose(slopes(2*x+5,20),0,atol=1e-12)
    assert np.allclose(slopes(np.ones(87),20),0,atol=1e-12)
    y = np.where(x<44,2*x,88-3*(x-44))
    assert np.isclose(slopes(y,20)[44-20],-5,atol=1e-12)
    assert np.allclose(slopes(y+103,20),slopes(y,20))
    a=null_maxima(y,block=5,draws=25,seed=8)
    b=null_maxima(y,block=5,draws=25,seed=8)
    assert np.array_equal(a,b) and np.isfinite(a).all() and (a>=0).all()
    assert len(circular_block_indices(87,5,np.random.default_rng(1)))==87
    for bad in [np.full(39,1.), np.array([np.nan]*87)]:
        try: max_stat(bad)
        except ValueError: pass
        else: raise AssertionError("invalid series accepted")
    print("PASS: candidate count, exact break, invariances, reproducibility, finite outputs, invalid inputs")

if __name__=="__main__": test()
