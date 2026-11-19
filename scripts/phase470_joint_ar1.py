"""Exact joint Gaussian AR(1) covariance for overlapping placebo contrasts.

Analytical illustration only. No SEC observations are read.
"""
import math


def weights(n, split):
    if not isinstance(n, int) or not isinstance(split, int) or not 1 <= split < n:
        raise ValueError('invalid sample length or split')
    return tuple(-1 / split if i < split else 1 / (n - split) for i in range(n))


def covariance(n=40, splits=(10, 20, 30), rho=0.5):
    if not -1 < rho < 1 or len(set(splits)) != len(splits):
        raise ValueError('invalid rho or repeated split')
    ws = [weights(n, k) for k in splits]
    return tuple(tuple(math.fsum(a[i] * b[j] * rho ** abs(i-j)
                         for i in range(n) for j in range(n)) for b in ws) for a in ws)


def correlation(matrix):
    if any(matrix[i][i] <= 0 for i in range(len(matrix))):
        raise ValueError('nonpositive diagonal')
    return tuple(tuple(x / math.sqrt(matrix[i][i] * matrix[j][j])
                       for j, x in enumerate(row)) for i, row in enumerate(matrix))


if __name__ == '__main__':
    for rho in (0, 0.3, 0.5, 0.8):
        v = covariance(rho=rho)
        c = correlation(v)
        print(f'{rho:.1f} variances={[round(v[i][i], 8) for i in range(3)]} '
              f'corr10_20={c[0][1]:.8f} corr10_30={c[0][2]:.8f}')
