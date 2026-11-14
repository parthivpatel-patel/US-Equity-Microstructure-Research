"""Exact finite-window correlation under stationary AR(1) daily shocks.

Constructed benchmark only; no observed SEC data or calibrated p-values.
"""
from fractions import Fraction

def covariance(lag, half_window=5, rho=Fraction(0)):
    if type(lag) is not int or lag < 0:
        raise ValueError('lag must be a nonnegative integer')
    if type(half_window) is not int or half_window < 1 or half_window > 100:
        raise ValueError('half_window must be integer in [1,100]')
    if isinstance(rho, bool) or not isinstance(rho, (int, Fraction)):
        raise ValueError('rho must be an exact integer or Fraction')
    rho = Fraction(rho)
    if abs(rho) >= 1:
        raise ValueError('stationarity requires abs(rho) < 1')
    w = [-1] * half_window + [1] * half_window
    return sum((w[i] * w[j] * rho ** abs(i - j - lag)
                for i in range(len(w)) for j in range(len(w))), Fraction(0))

def correlation(lag, half_window=5, rho=Fraction(0)):
    return covariance(lag, half_window, rho) / covariance(0, half_window, rho)

def report():
    return {str(r): {str(lag): str(correlation(lag, 5, r))
                     for lag in (0, 1, 2, 3, 4, 5, 10)}
            for r in (Fraction(-1, 2), Fraction(0), Fraction(1, 2))}

if __name__ == '__main__':
    import json
    print(json.dumps(report(), indent=2))
