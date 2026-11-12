# Phase 322 — Frozen placebo summary fails a joint feasibility check (2026-11-12)

## Source and reproducible calculation

Source: `results/phase130_summary.csv` on public `main`, read before this report was created. The published count row states event contrast `d=-0.7346606598677254` percentage points, 78 placebo windows, lower-tail count `L=2`, absolute-extreme count `A=2`, minimum `-1.4475738789418606`, and maximum `+1.0538523294152946`.

**Conditional on the column labels meaning that the extrema and counts refer to the same 78 numerical placebo contrasts and that 'at least as negative' means x <= d, these five values are jointly impossible.** Because d < 0, every one of the L=2 observations satisfying x <= d also satisfies |x| >= |d|. Separately, the observed maximum +1.0538523294152946 is greater than |d|=0.7346606598677254; that maximum cannot be one of the two negative-tail observations. Therefore the absolute-extreme count must be **at least 3**, but the published value is 2. This argument does not require independent windows, no ties, rounding assumptions, or raw SEC records.

A second correction applies to the volume row. For positive `d=+0.626597999820323`, `L=#{x<=d}=48` and `n=78`. Consequently exactly 30 observations satisfy `x>d`, and therefore `R=#{x>=d} >= 30`. The previously reported unconditional lower bound 28 (Phases 318–320) is conservative but not the tightest available bound. With `A=76` and a reported minimum below `-d`, at least one absolute-extreme observation is negative, giving `R<=75`. Thus **30–75** is a tighter necessary range, *provided all statistics use the same placebo set and these exact tail definitions*. This is not an estimate or a calibrated p-value.

## Reproduction with standard-library Python

```python
import csv
from decimal import Decimal
with open("results/phase130_summary.csv", newline="") as f:
    rows = {r["outcome"]: r for r in csv.DictReader(f)}
c = rows["count"]
d = Decimal(c["nov_minus_oct_pp"])
L = int(c["pre_placebo_at_least_as_negative"])
A = int(c["pre_placebo_at_least_as_extreme_absolute"])
mx = Decimal(c["pre_placebo_max_pp"])
assert d < 0 and mx > abs(d)
assert A < L + 1  # proves inconsistency if same 78 contrasts
v = rows["volume"]
dv = Decimal(v["nov_minus_oct_pp"])
Lv = int(v["pre_placebo_at_least_as_negative"])
Av = int(v["pre_placebo_at_least_as_extreme_absolute"])
n = int(v["pre_placebo_n"])
mn = Decimal(v["pre_placebo_min_pp"])
assert dv > 0 and mn < -dv
assert (n-Lv, Av-1) == (30, 75)
print("Count aggregate inconsistency confirmed; volume necessary bound: 30–75")
```

This code checks **published summary arithmetic only**, not the underlying 78 windows. No third-party data is redistributed.

## Interpretation and publication gate

The count contradiction might reflect a mislabeled column, different placebo window populations, a filtering inconsistency, or an upstream calculation/reporting error. It **does not** identify which explanation is correct. Previous Phases 317–321 checked individual bounds or synthetic sequences, but did not reject this joint inconsistency. Their count-row directional conclusions should be treated as **suspended pending reconciliation**. Do not silently edit the source CSV or treat Phase 320's count bound as an admissible empirical interval.

Next: trace the Phase 130 summary producer, recover the exact 78 dated placebo values and their filters, verify extrema and both tail counts on the identical set, and test chronology against the October 2025 announcement. Then authenticate SEC source bytes and historical round-lot assignments before any pretrend/DiD or dependence-aware causal interpretation. The September pretrends, October placebo, matching/weighting sensitivity, common-date dependence, and 129 historical ZIP inventory remain unresolved. The November 14 target is not a validation certificate.
