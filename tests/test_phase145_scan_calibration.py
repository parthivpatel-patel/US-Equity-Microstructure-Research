"""Phase 145: independent deterministic tests of published Phase 143 scan mechanics.
No market data or empirical significance claims.
"""
import numpy as np

def direct_scan(y, window=20):
    y = np.asarray(y, dtype=float)
    if y.ndim != 1 or len(y) < 2 * window or not np.isfinite(y).all():
        raise ValueError('invalid series')
    x = np.arange(window, dtype=float)
    z = x - x.mean()
    denom = z @ z
    return np.array([z @ y[i:i+window] / denom - z @ y[i-window:i] / denom
                     for i in range(window, len(y)-window+1)])

def convolution_scan(y, window=20):
    y = np.asarray(y, dtype=float)
    x = np.arange(window, dtype=float)
    w = (x-x.mean()) / np.sum((x-x.mean())**2)
    s = np.convolve(y, w[::-1], mode='valid')
    return s[window:] - s[:-window]

def monte_carlo_tail(observed, null_maxima):
    """Finite Monte Carlo upper-tail rank with plus-one correction.
    Valid as a calibrated p-value only under appropriate null exchangeability.
    """
    a = np.asarray(null_maxima, dtype=float)
    if a.ndim != 1 or not len(a) or not np.isfinite(a).all() or not np.isfinite(observed) or observed < 0 or (a < 0).any():
        raise ValueError('invalid maxima')
    return (1 + int(np.count_nonzero(a >= observed))) / (len(a) + 1)

def test():
    rng = np.random.default_rng(145)
    checked = 0
    for n in [40, 41, 67, 87, 106]:
        for window in [3, 5, 10, 20]:
            if n < 2*window: continue
            for _ in range(10):
                y = rng.normal(size=n).cumsum() + .1*np.arange(n)
                d = direct_scan(y,window)
                c = convolution_scan(y,window)
                assert len(d) == n-2*window+1
                np.testing.assert_allclose(d,c,atol=1e-12,rtol=1e-12)
                np.testing.assert_allclose(direct_scan(y+300+2*np.arange(n),window),d,atol=1e-12)
                checked += 1
    assert len(direct_scan(np.arange(87.),20)) == 48
    assert monte_carlo_tail(2,[0,1,2,3]) == 3/5
    assert monte_carlo_tail(10,[0,1,2,3]) == 1/5
    assert monte_carlo_tail(0,[0,1,2,3]) == 1
    for invalid in [[], [float('nan')], [-1,0]]:
        try: monte_carlo_tail(1,invalid)
        except ValueError: pass
        else: raise AssertionError('invalid maxima accepted')
    print(f'PASS: {checked} randomized direct/convolution comparisons, linear invariance, candidate counts, finite-simulation tail conventions')

if __name__ == '__main__': test()
