# Phase 170 — Fixed-calendar missingness admission (2026-11-05)

## Scope and finding

Phase 169 reports coverage only for dates observed in at least one input cell. Thus a trading date for which *all* treatment-arm cells are absent is omitted entirely, potentially overstating calendar coverage. This is a source-code property of Phase 169, not an observed defect in SEC data.

The new independent diagnostic in `tests/test_phase170_fixed_calendar_coverage.py` requires explicit, externally authenticated expected trading dates and a predetermined matched-group roster. It reports complete, partial and absent group pairs for **every** expected date, including dates with zero observed rows. It rejects dates outside the roster, duplicate observations, malformed dates, nonfinite outcomes and invalid arms. It deliberately does not equate weekdays with exchange trading days.

## Constructed counterexample

Expected dates: October 1, 2, 3, 2025. Groups: A, B. October 1 contains both arms for A; October 2 contains only control for B; October 3 has no observations. The resulting complete-pair coverage is respectively 0.5, 0, 0. The October 3 row is omitted by the earlier observed-date-only algorithm but explicitly present here. No historical market inference follows.

A local prototype of this method passed ten Python unittest cases on November 5, 2026. The published companion is a separate, compact implementation of the same checks; its exact fresh-checkout execution has not yet been verified.

## Required empirical gates

1. Authenticate SEC source archives, checksums, schema, licensing and the actual security/exchange/date panel.
2. Authenticate historical round-lot treatment from UTP notices and contemporaneous reference prices; do not silently treat provisional assignments as ground truth.
3. Establish expected exchange trading dates and matched-group rosters *before* outcome filtering. Audit missing entire dates, partial pairs and date-by-exchange missingness.
4. Re-estimate September pretrends and multiple October 2025 placebo cutoffs; preserve the substantial October placebo warning and do not assert a reform effect.
5. Compare balanced and available-case groups, security/exchange controls, trade-count versus volume outcomes, weighting/selection sensitivity and common-date plus serial-dependence-aware inference.
6. Recover historical ZIPs, scripts, figures and manuscripts only after inspecting provenance, redistribution rights, contents and repository limits.

## Provenance and publication limits

All Phase 170 numbers are deterministic fixtures, not SEC market estimates. No source archives, authenticated treatment snapshots, historical ZIPs, or real-data figures were imported this session. The complete historical artifact inventory remains unverified; absence from this session is not proof the artifacts do not exist elsewhere. No causal effect is established. November 14, 2026 is a conditional publication target.
