"""Validate joint feasibility of frozen historical-placebo summary rows.

No SEC source records are loaded. Fail closed when a negative event contrast
has lower-tail observations plus a distinct positive absolute-extreme maximum.
"""
import csv
from decimal import Decimal
from pathlib import Path


def audit_row(row):
    d = Decimal(row["nov_minus_oct_pp"])
    n = int(row["pre_placebo_n"])
    lower = int(row["pre_placebo_at_least_as_negative"])
    absolute = int(row["pre_placebo_at_least_as_extreme_absolute"])
    minimum = Decimal(row["pre_placebo_min_pp"])
    maximum = Decimal(row["pre_placebo_max_pp"])
    if not all(x.is_finite() for x in (d, minimum, maximum)):
        raise ValueError("non-finite value")
    if not (0 <= lower <= n and 0 <= absolute <= n and minimum <= maximum):
        raise ValueError("invalid counts or extrema")
    if d < 0 and maximum >= abs(d) and absolute < lower + 1:
        return "INCONSISTENT: positive maximum adds distinct absolute extreme"
    if d > 0 and minimum <= -d and absolute < (n - lower) + 1:
        return "INCONSISTENT: negative minimum adds distinct absolute extreme"
    return "NOT DISPROVED (not independently validated)"


def main():
    with Path("results/phase130_summary.csv").open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    for row in rows:
        print(row["outcome"], audit_row(row))


if __name__ == "__main__":
    main()
