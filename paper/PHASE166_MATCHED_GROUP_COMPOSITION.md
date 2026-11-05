# Phase 166: Matched-group composition drift audit

Date: 2026-11-05. Scope: independent round-lot reform research only.

## Finding

The Phase 165 available-case matched-group/date contrast averages over whichever matched groups are present on a given date. A changing group roster can therefore generate an apparent discontinuity even when every group's underlying treated-minus-control contrast is constant.

A deterministic four-date fixture includes group A (contrast 0 throughout) and group B (contrast 10, observed only after the cutoff). Available-case date contrasts are [0, 0, 5, 5], implying a spurious +5 pre/post difference. Requiring the same complete groups on every date leaves group A only and produces [0, 0, 0, 0]. The example is synthetic and not an SEC estimate.

## Verification

Six local unittest cases passed on 2026-11-05: composition counterexample, complete panel, duplicate cell rejection, nonfinite outcome rejection, absence of balanced groups, and missing pre/post period. Run `python -m unittest tests/test_phase166_composition.py -v` from the repository root (or `python tests/test_phase166_composition.py`). The published source was reconstructed from the tested prototype; a fresh checkout run is still required.

## Identification consequences

Report the matched-group roster on every calendar date, pre/post retention by treatment and exchange, and both fixed-roster and available-case estimates. Fixed-roster analysis changes the estimand and may select survivors; it is a sensitivity analysis, not a universal fix. Neither approach authenticates the 2025 Nasdaq treatment assignment. Security/exchange controls, placebo windows, September pretrends, common-date shocks, and serial dependence remain necessary. Date-block resampling alone does not address matched-group sampling uncertainty.

## Provenance and remaining work

This session did not recover the SEC source archives, Nasdaq snapshots, original daily security/exchange observations, or the historical ZIP collection. No empirical estimates or causal claims are made. The historical Phase 2 panel is not equivalent to a daily exchange panel. Next: authenticate original daily observations and report actual group/date composition before placebo and pretrend re-estimation. November 14 publication remains conditional.
