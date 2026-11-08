# Phase 239 — Executed HAC bandwidth fixture audit (2026-11-08)

## Scope
This is a **synthetic numerical verification**, not an empirical SEC estimate. I inspected the published `scripts/phase224_common_date_hac.py`, `scripts/phase238_hac_bandwidth_sensitivity.py`, and `tests/test_phase238_hac_bandwidth_sensitivity.py` via the connected GitHub interface. I reconstructed their relevant executable logic in a local isolated Python workspace and executed the six Phase 238 test scenarios against that reconstruction. **The repository's original test files were not executed directly from a Git clone.** No claim is made that the whole repository test suite passed.

## Local execution
Command: `python -m unittest discover -s tests -v`. Result: **6 tests passed**, no errors, Python unittest. The scenarios check point-estimate invariance, nonnegative standard errors, duplicate/unsorted/invalid bandwidth rejection, and incomplete-panel rejection. The local test reconstruction simplified some assertions and is not a byte-identical test of the published source.

For six synthetic ordered dates (2025-09-02, 03, 04, 05, 08, 09), early values (0.1, 0.2, 0.3), and late values (0.4, 0.5, 0.6), the reconstructed Phase 224/238 logic produced:

| Bartlett bandwidth | Late-minus-early difference | HAC standard error |
|---:|---:|---:|
| 0 | 0.30000000000000004 | 0.06666666666666667 |
| 1 | 0.30000000000000004 | 0.07453559924999298 |
| 2 | 0.30000000000000004 | 0.06666666666666667 |
| 3 | 0.30000000000000004 | 0.05270462766947299 |
| 4 | 0.30000000000000004 | 0.042163702135578386 |
| 5 | 0.30000000000000004 | 0.03849001794597504 |

These are **synthetic fixture outputs only**, not market observations, not p-values, and not a calibration of appropriate bandwidth. With six observations, lag-five uncertainty is especially fragile; the small standard error is not evidence of precision. Point estimates remain unchanged because bandwidth modifies the covariance calculation, not the mean contrast. Equal-cell and pooled-count series were deliberately identical in this fixture, so this exercise does not test weighting sensitivity.

## Identification and provenance status
- Historical SEC observation authenticity: **not verified** in this session.
- Exchange-session roster authenticity: **not verified**.
- Historical round-lot treatment classification: **not verified**.
- September pretrends and substantial October placebo: **unresolved**.
- Security clustering, matched-group and common-date dependence inference on actual observations: **not executed**.
- Historical ZIPs and previous paper/figure assets: **not available for verified import**; no complete inventory claim.
- Causal effect: **not established**.

## Next actions
Obtain source-authenticated panel and calendar; run the **exact repository test suite** rather than reconstructed copies; compare matched-security/common-date HAC with security-level cluster or block-bootstrap inference on a frozen roster; rerun September pretrends and October placebo before any causal wording. The November 14, 2026 target remains conditional.
