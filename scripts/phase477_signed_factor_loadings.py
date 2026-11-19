"""Phase 477: exact common-date factor cancellation under heterogeneous matched-pair loadings.
Constructed mathematical benchmark, not empirical SEC observations.
Python 3 standard library only.
"""
from math import sqrt

T = 40
WEIGHTS = [-1 / 20] * 20 + [1 / 20] * 20

def q(rho):
    if not -1 < rho < 1:
        raise ValueError("AR(1) parameter must be stationary")
    return sum(WEIGHTS[i] * WEIGHTS[j] * rho ** abs(i - j)
               for i in range(T) for j in range(T))

def se_inflation(loadings, rho_factor=0.5, rho_pair=0.5):
    if not loadings:
        raise ValueError("Need at least one matched pair")
    n = len(loadings)
    avg = sum(loadings) / n
    return sqrt(1 + avg * avg * n * q(rho_factor) / (2 * q(rho_pair)))

def main():
    n = 68
    cases = {
        "uniform_positive": [0.5] * n,
        "balanced_signs": [0.5] * 34 + [-0.5] * 34,
        "three_quarter_positive": [0.5] * 51 + [-0.5] * 17,
        "single_positive": [0.5] + [0.0] * 67,
    }
    assert abs(q(0) - 0.1) < 1e-12
    assert se_inflation(cases["balanced_signs"]) == 1
    assert abs(se_inflation(cases["uniform_positive"]) -
               sqrt(1 + 0.25 * n / 2)) < 1e-12
    for name, values in cases.items():
        print(f"{name},{sum(values)/n:.8f},{se_inflation(values):.8f}")

if __name__ == "__main__":
    main()
