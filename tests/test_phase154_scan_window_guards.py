"""Independent shape and minimum-window audit of Phase 153's adjacent-slope scan.

Synthetic tests only; no market data.
"""
import numpy as np


def guarded_scan(y, window):
    y = np.asarray(y, dtype=float)
    if y.ndim != 1 or y.size < 2 or not np.all(np.isfinite(y)):
        raise ValueError('y must be a finite one-dimensional series of length >= 2')
    if isinstance(window, (bool, np.bool_)) or not isinstance(window, (int, np.integer)):
        raise ValueError('window must be an integer')
    if window < 2 or 2 * window > y.size:
        raise ValueError('window must be >= 2 and leave at least two complete windows')
    x = np.arange(window, dtype=float)
    w = (x - x.mean()) / np.sum((x - x.mean()) ** 2)
    slopes = np.convolve(y, w[::-1], mode='valid')
    return slopes[window:] - slopes[:-window]


def direct_scan(y, window):
    x = np.arange(window, dtype=float)
    x -= x.mean()
    den = x @ x
    return np.array([((y[i+window:i+2*window] @ x) - (y[i:i+window] @ x)) / den
                     for i in range(len(y) - 2*window + 1)])


def test():
    rng = np.random.default_rng(1542026)
    cases = 0
    for n in (4, 5, 12, 40, 87, 106):
        for w in range(2, n//2 + 1):
            for _ in range(5):
                y = rng.normal(size=n)
                actual = guarded_scan(y, w)
                expected = direct_scan(y, w)
                assert actual.shape == (n - 2*w + 1,)
                np.testing.assert_allclose(actual, expected, rtol=0, atol=2e-13)
                cases += 1
    invalid = [(np.arange(8.), 1), (np.arange(8.), 0), (np.arange(8.), 5),
               (np.arange(8.), 2.5), (np.arange(8.), True),
               (np.array([0., np.nan, 2., 3.]), 2),
               (np.ones((2, 4)), 2), (np.arange(1.), 2)]
    for y, w in invalid:
        try:
            guarded_scan(y, w)
        except ValueError:
            continue
        raise AssertionError(f'failed to reject {w!r} / {np.shape(y)}')
    print(f'PASS {cases} independent OLS comparisons; {len(invalid)} invalid cases rejected')

if __name__ == '__main__':
    test()
