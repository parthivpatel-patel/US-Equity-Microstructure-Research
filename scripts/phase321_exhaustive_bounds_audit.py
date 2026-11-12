"""Exhaustive finite-grid falsification check for Phase 320 placebo bounds.

Synthetic mathematical validation only; does not reproduce SEC observations.
Run: python scripts/phase321_exhaustive_bounds_audit.py
"""
from itertools import product

def claimed_bounds(d, n, lower, absolute, minimum, maximum):
    if d > 0:
        lo = max(0, absolute - lower, int(maximum >= d))
        hi = min(absolute - int(minimum <= -d), n)
    else:
        if absolute < lower:
            raise ValueError("inconsistent counts")
        lo = n - lower
        hi = n - int(minimum < d)
        if maximum < d:
            hi = 0
    if lo > hi:
        raise ValueError("inconsistent summary")
    return lo, hi

def audit():
    outcomes = []
    for d in (-2, 2):
        for n in range(1, 6):
            groups = {}
            for xs in product(range(-3, 4), repeat=n):
                lower = sum(x <= d for x in xs)
                absolute = sum(abs(x) >= abs(d) for x in xs)
                right = sum(x >= d for x in xs)
                key = (d, n, lower, absolute, min(xs), max(xs))
                groups.setdefault(key, set()).add(right)
            for key, observed in groups.items():
                lo, hi = claimed_bounds(*key)
                assert lo <= min(observed) and max(observed) <= hi, (
                    key, sorted(observed), (lo, hi)
                )
            outcomes.append((d, n, len(groups)))
    return outcomes

if __name__ == "__main__":
    results = audit()
    for d, n, groups in results:
        print(f"contrast={d:+d}, n={n}, distinct summaries={groups}: PASS")
    print(f"PASS: {sum(x[2] for x in results)} distinct summary configurations")
