"""Audit logical feasibility of placebo tail counts, without source observations.

All thresholds use exact Decimal values from the published CSV.
The lower count L is # {x <= d}; absolute count A is # {|x| >= |d|}.
This is a necessary-condition gate, not an empirical estimator.
"""
import csv
from decimal import Decimal
from pathlib import Path


def check(row):
    d = Decimal(row["nov_minus_oct_pp"])
    lo = Decimal(row["pre_placebo_min_pp"])
    hi = Decimal(row["pre_placebo_max_pp"])
    n = int(row["pre_placebo_n"])
    L = int(row["pre_placebo_at_least_as_negative"])
    A = int(row["pre_placebo_at_least_as_extreme_absolute"])
    if not all(z.is_finite() for z in (d, lo, hi)) or d == 0:
        raise ValueError("nonfinite or zero event contrast")
    if n < 1 or not (0 <= L <= n and 0 <= A <= n and lo <= hi):
        raise ValueError("invalid sample size, counts, or extrema")
    if lo > d and L:
        raise ValueError("minimum rules out reported lower count")
    if hi <= d and L != n:
        raise ValueError("maximum rules out reported upper count")
    if lo <= d and L == 0:
        raise ValueError("minimum requires a lower observation")
    if hi > d and L == n:
        raise ValueError("maximum requires an upper observation")
    # Partition by x<=d and x>d. For d<0, all x<=d are absolute
    # extremes; for d>0, all x>d are absolute extremes.
    bound = L if d < 0 else n - L
    if d < 0 and hi >= -d:
        bound += 1  # positive maximum lies outside the lower partition
    if d > 0 and lo <= -d:
        bound += 1  # negative minimum lies outside the upper partition
    return {"minimum_absolute_extremes": bound,
            "reported_absolute_extremes": A,
            "consistent_with_necessary_conditions": A >= bound}


def main():
    with Path("results/phase130_summary.csv").open(newline="") as f:
        for row in csv.DictReader(f):
            print(row["outcome"], check(row))


if __name__ == "__main__":
    main()
