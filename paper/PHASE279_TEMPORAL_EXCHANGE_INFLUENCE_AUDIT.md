# Phase 279 — Temporal stability of exchange influence (2026-11-09)

## Verified local diagnostic

A standalone Python prototype split a fixed three-pair, two-exchange synthetic panel into early and late periods, computed pair-weighted and exchange-equal means, and recomputed both after omitting each exchange. Nine deterministic unittest cases passed locally (zero failures), including duplicate/unsorted dates, missing exchange, nonfinite outcome, Boolean pair count, invalid cutoff, empty split and cutoff-boundary assignment. The prototype and tests were **not uploaded**; this report does not claim the exact repository checkout passed those tests.

Constructed input: exchange X has two pairs and exchange Y one. On two early dates, X=-2 and Y=5; on two late dates, X=1 and Y=-1. Pair-weighted full-period means are 1/3 in **both** windows, while omitting Y changes the mean from -2 to +1 (late-minus-early +3). Thus an unchanged aggregate contrast can mask substantial exchange-composition heterogeneity. These are arithmetic illustrations, **not SEC observations**.

## Methodological consequence

A single full-period leave-one-exchange-out estimate (Phase 278) does not diagnose whether exchange influence changes over time. For authenticated data, predeclare September/October windows, use a fixed pair roster and independently authenticated session calendar, and report full/omitted estimates by window alongside the difference of window contrasts. Require the same underlying matched pairs across windows; do not treat exchange-equal weighting as a causal correction.

Temporal stability is descriptive only. Serially correlated dates, security-level dependence, exchange clustering, and common-date shocks invalidate naive independent-day standard errors. A bootstrap must resample matched security groups and common dates in a design consistent with their dependence, with HAC lag sensitivity as a separate robustness diagnostic. Never treat synthetic arithmetic as historical evidence.

## Admission blockers and unpublished inventory

Historical SEC source checksums, redistribution permissions, session-calendar authentication, original security/exchange observations, treatment assignments at the November 3, 2025 cutoff, and fixed matched roster remain unverified in this session. September pretrends and the substantial October 2025 placebo warning remain unresolved. No causal effect is established.

Previously recovered research ZIP archives, earlier manuscripts and charts remain **unimported** and have no complete verified inventory. Phase 279 standalone local prototype and tests also remain unpublished. No historical figure or coefficient was produced.

Next: retrieve and authenticate source-data manifests; inventory recovered archives and licenses; rerun published Phase 269–278 code in a clean checkout; integrate and publish the Phase 279 prototype after repository tests; only then estimate predeclared historical pretrends/placebos.
