# Phase 133 — Monthly pretrend and matched-group influence diagnostics

Executed on November 3, 2026 from the recovered Phase 131 processed panel. **Exploratory, not causal.** Input SHA-256: `6347d66cd7fa7ffa070b60529935e7ca9c93ef5c7f8dc61050fba33582f9aea1`. 14,416 rows, 68 matched groups, 106 dates, two outcomes; no missing or duplicate group-date-outcome cells.

## Monthly equal-weighted group mean contrasts (percentage points)

| Month | Count | Volume | Trading dates |
|---|---:|---:|---:|
| July | 3.863707 | 6.164102 | 22 |
| August | 3.598751 | 5.729725 | 21 |
| September | 5.228904 | 6.023019 | 21 |
| October | 3.266191 | 4.202444 | 23 |
| November | 0.426117 | 2.180610 | 19 |

September minus August: **+1.630152 pp** for count (48 of 68 groups positive) and **+0.293294 pp** for volume (40 of 68 positive). These are descriptive *within-group contrast changes*, not treated-versus-control parallel-trend tests. Their presence reinforces concerns about strong pre-event movement.

## Five-trading-day event contrasts

| Outcome | Date | Mean (pp) | Median group (pp) | Negative groups | Leave-one-group-out mean range (pp) |
|---|---|---:|---:|---:|---|
| Count | October 6 | -0.601120 | -0.451629 | 37/68 | [-0.729741, -0.440218] |
| Count | November 3 | -1.335781 | -1.843558 | 45/68 | [-1.470935, -1.042633] |
| Volume | October 6 | -0.633537 | -0.909776 | 39/68 | [-0.778761, -0.446211] |
| Volume | November 3 | -0.006939 | -0.095510 | 34/68 | [-0.233569, +0.238752] |

October 6 uses September 29–October 10; November 3 uses October 27–November 7. These windows are not pure unaffected counterfactuals. In particular October 1 was an information event. The November volume mean is extremely close to zero and changes sign when one group is removed; the November count mean stays negative under single-group deletion but is not a causal estimate.

## Limitations and next tests

The input is a **processed contrast panel**, not authenticated raw SEC exchange-by-security data. Group labels are securities, but the venue-level source decomposition, treatment-classification history, corporate actions, weights, and complete-case selection are not verified. Monthly contrasts may reflect both treatment and control movements. Cross-group dispersion does not handle common date shocks, serial dependence, or multiple-testing selection. A valid parallel-trends assessment requires authenticated treated and matched-control security-by-exchange outcomes, frozen classifications, and common-date dependence-aware uncertainty.

The source input remains absent from public GitHub pending provenance and redistribution checks. The script can be run locally with the recovered Phase 131 package. All outputs are from an actual Python run against that package; see the two published CSV files and their SHA-256 manifest.
