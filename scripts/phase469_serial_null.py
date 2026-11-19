"""Exact Gaussian AR(1) null calibration for a two-period placebo contrast."""
import math

def calibration(n=40, split=20, rho=0.5):
    if not (2 <= n and 1 <= split < n and -1 < rho < 1):
        raise ValueError("invalid design")
    w = [-1/split]*split + [1/(n-split)]*(n-split)
    variance = sum(w[i]*w[j]*rho**abs(i-j) for i in range(n) for j in range(n))
    iid_variance = sum(x*x for x in w)
    ratio = variance/iid_variance
    size = math.erfc(1.959963984540054/math.sqrt(2*ratio))
    return variance, iid_variance, ratio, size

if __name__ == "__main__":
    for rho in (0.0, 0.3, 0.5, 0.8):
        print(rho, calibration(rho=rho))
