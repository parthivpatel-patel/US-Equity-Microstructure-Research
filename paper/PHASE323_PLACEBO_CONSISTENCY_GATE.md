# Phase 323 — Fail-closed placebo summary consistency gate (2026-11-12)

## Inputs and scope
Read the existing public `results/phase130_summary.csv` before adding `scripts/phase323_placebo_joint_gate.py`. This script is standard-library Python and reads the published CSV directly; it does not infer underlying SEC data, generate charts, or redistribute third-party datasets.

## New reproducibility control
The gate validates finite numerical inputs, nonnegative bounded counts and ordered extrema. It reports a **logical contradiction** when a negative event contrast has L lower-tail observations but a distinct positive maximum at least as large as the absolute event contrast and the claimed absolute-extreme count is less than L+1. It applies the symmetric test to a positive event contrast and a negative minimum.

For the published count row: d = -0.7346606598677254, L = 2, A = 2, maximum = +1.0538523294152946. Hence A must be at least 3 under a common 78-window population, but the file says 2. The row fails the gate. This independently restates the Phase 322 contradiction in an executable check that can be rerun when data are updated. **Do not repair the CSV by changing a number without recovering the source windows.**

For the published volume row, d = +0.626597999820323, L = 48, A = 76, minimum = -1.8665501312689659, n = 78. The symmetric necessary bound is A >= (n-L)+1 = 31, so this particular check does not disprove the row. Passing the gate does not authenticate the row or imply that its values are jointly attainable.

## Reproduction
From the repository root, run `python scripts/phase323_placebo_joint_gate.py`. Expected classification from the read CSV is `count INCONSISTENT` and `volume NOT DISPROVED`. These are **expected classifications based on inspected inputs**, not a claim of execution against a freshly checked-out repository.

## Research implications
The count-row historical placebo statistics are unusable as a jointly valid descriptive distribution until the original 78 dated window estimates, filters and producer are recovered. The September pretrends, October placebo warning, round-lot treatment authentication, matched-group and weighting choices, security/exchange controls, common-date and serial-dependence-aware inference remain unresolved. This gate does not advance causal identification. The November 14 manuscript target remains conditional, and historical ZIP inventory and redistribution rights still require reconciliation.
