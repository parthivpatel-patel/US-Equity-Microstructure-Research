# Phase 315 — Frozen Phase 130 summary reconciliation (2026-11-12)

## Scope and verification
Read existing published `results/phase130_summary.csv` and `results/phase130_group_sensitivity.csv` via the connected GitHub file API. Reconstructed the exact displayed CSV bytes locally and executed a standard-library Decimal audit against them. Five deterministic unit tests passed locally (Python unittest, 5/5); the full repository regression suite and CI on the new published files have **not** been executed in this session. Script: `scripts/phase315_frozen_summary_audit.py`; tests: `tests/test_phase315_frozen_summary_audit.py`.

Reproduce from repository root:

```bash
python -m unittest tests/test_phase315_frozen_summary_audit.py
python -m scripts.phase315_frozen_summary_audit results/phase130_summary.csv results/phase130_group_sensitivity.csv
```

## Frozen-summary checks (percentage points)
| Outcome | November | October | November minus October | Reported group bootstrap interval | Contains zero | Absolute-extreme historical windows |
| --- | ---: | ---: | ---: | --- | --- | --- |
| Hidden count | -1.3357808794 | -0.6011202195 | -0.7346606599 | [-2.0939912970, 0.5739443327] | Yes | 2 / 78 |
| Hidden volume | -0.0069385870 | -0.6335365868 | +0.6265979998 | [-0.9362642705, 2.2295428794] | Yes | 76 / 78 |

The arithmetic reconciles to within 1e-12 percentage points between the two existing published summaries. The outcome definitions have **opposite signs** for the November-minus-October contrast. Both published group-bootstrap intervals include zero. These are audits of *inherited frozen output tables*, not independently recomputed estimators, and the bootstrap sampling scheme has not been independently certified.

The 2/78 and 76/78 fractions are **descriptive**, not calibrated p-values: placebo windows overlap, were considered post hoc, and may contain information events. The October 1 announcement is not a pure no-information placebo. September pretrends, selection and weighting sensitivity, treatment assignment authentication, common-date serial dependence, and security/exchange composition remain material identification concerns.

## Data provenance and publication gate
No raw SEC observations, treatment-source files, licensed archives, or synthetic figures were added. The historical archive reconciliation remains incomplete (see `provenance/PHASE314_PUBLIC_TREE_INVENTORY_2026-11-12.md`). Source-level authentication and end-to-end replication remain outstanding; **no causal inference or publication-ready validation is claimed**. November 14 is a target, not evidence of completion.

Next: exact-checkout regression testing, archival hash/license crosswalk, authenticated panel pretrend and placebo replication with matched common-date and dependence-aware inference.
