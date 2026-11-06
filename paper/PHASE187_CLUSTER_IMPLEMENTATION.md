# Phase 187 — Published two-way cluster implementation (2026-11-06)

## Scope and verified work

Published a balanced matched-group × placebo-date intercept-only two-way CR1 variance estimator and deterministic tests, extending the Phase 186 methodological checkpoint. The estimator calculates group-cluster and date-cluster covariance components and subtracts the group/date intersection component. Negative combined variance returns a null standard error with an explicit warning rather than silently clipping it.

A closely equivalent local prototype passed 10 deterministic tests on constructed observations (balanced input, translation and row-order invariance, constant outcomes, duplicates, unbalanced panels, invalid dates, nonfinite values, insufficient clusters, and schema mismatch). **A fresh checkout run of the exact published version has not been performed.** No empirical SEC data were used.

Run from the repository root:

```bash
python -m unittest tests/test_phase187_cluster.py
python scripts/phase187_cluster.py path/to/group_date_contrasts.csv
```

Required CSV columns: `matched_group_id,placebo_date,contrast_pp`. The input must be a balanced, unique group-date grid representing **one** outcome and **one** prespecified event-window specification. Do not pool overlapping windows or count and volume in one invocation.

## Statistical interpretation and limitations

For G matched groups, T dates, and residuals e[g,t]=y[g,t]-mean(y), the intercept-only variance is:

```
V = (G/(G-1) * sum_g (sum_t e[g,t])^2
   + T/(T-1) * sum_t (sum_g e[g,t])^2
   - (G*T)/(G*T-1) * sum_(g,t) e[g,t]^2) / (G*T)^2
```

This is a descriptive small-sample-corrected two-way cluster covariance estimator, **not** a causal treatment-effect standard error. Few-cluster inference, overlapping placebo windows, cross-security spillovers, exchange composition, security effects, date effects, treatment timing and selection must be handled separately. It does not replace an identified panel regression or validate confidence intervals. Constructed test data must never be presented as historical market evidence.

## Identification and provenance blockers

The authenticated daily SEC source panel, historical round-lot treatment snapshot, fixed matched-group roster, actual placebo date memberships, and original research archives remain unavailable for this execution. Consequently **no historical coefficient or new SEC standard error was estimated**. The September pretrends and substantial October 2025 pre-reform movement remain major identification warnings; October 1 is not a clean no-information placebo. No causal effect established.

## Publication inventory delta

New public paths: `scripts/phase187_cluster.py`, `tests/test_phase187_cluster.py`, and this checkpoint. No historical ZIP/PDF/code/chart archive imported in this phase. An exhaustive inventory of older unpublished archives cannot be certified without the recovered archive files and hashes.

## Next task

Fresh-checkout test the exact published files; recover and checksum authentic SEC observations and historical eligibility snapshots; verify fixed matched-group and common-date rosters; then run two-way clustering alongside sensitivity to weighting, date-block bootstrap, and pretrend/placebo diagnostics. The November 14 publication target remains conditional.
