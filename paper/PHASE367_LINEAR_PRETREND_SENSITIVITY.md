# Phase 367 — Exact linear-pretrend contamination of five-session contrasts

Date: 2026-11-14. Status: mathematical diagnostic only, not an empirical SEC estimate.

## Identification warning
For a symmetric event comparison of the mean of sessions t through t+h−1 minus the mean of t−h through t−1, let the untreated outcome follow y_s = a + b*s. Then the difference of means equals exactly **h*b**, even with no event effect. For h=5, a pre-existing slope of 0.01 outcome units per trading session creates a 0.05-unit post-minus-pre contrast. This is a *constructed illustrative slope*, not an observed SEC slope. The conclusion holds regardless of intercept and without randomness.

A single trend slope cannot be assumed stable across September, October and November. Trend adjustment with a slope estimated using post-event outcomes may introduce additional bias; slope should be prespecified or estimated from an authenticated pre-event window with its uncertainty propagated. A zero adjusted contrast does not prove absence of an event effect; a nonzero contrast does not prove reform causality.

## Replication and validation
Run `python scripts/phase367_trend_contamination.py` and `PYTHONPATH=scripts python -m unittest discover -s tests -p 'test_phase367_trend_contamination.py' -v`. Seven deterministic local tests passed after correcting an overflow exception discovered in initial tests. They cover exact trends across multiple window lengths and slopes, intercept invariance, step preservation, negative trends and malformed input. The exact published checkout and full repository regression suite have not yet been run.

## Empirical gating and limitations
No original SEC rows or the 78 dated placebo outputs were available for this analysis. The substantial October placebo warning, September pretrends, Phase 130 contradiction, unauthenticated treatment assignments, exchange eligibility, selection/weighting sensitivity, common-date shocks and serial dependence all remain live blockers. Before reporting an empirical effect: authenticate source bytes and round-lot treatment, verify security/exchange/date coverage, estimate pretrend slopes with uncertainty, rerun all placebo dates, and use matched-group plus calendar/block dependence-aware inference. Historical research ZIPs and papers remain unimported/unverified here; do not assert a complete inventory.

**November 14, 2026 deadline missed. Manuscript uncertified. No causal claim.**
