# Phase 171 — Fixed-calendar pre/post coverage admission

Date: 2026-11-05. Scope: independent U.S. equity round-lot reform research. No GIG assets or datasets.

## Reproducible methodological result

Phase 170 reports coverage for every date in an externally supplied calendar, including entirely missing dates. Phase 171 adds a period-specific coverage gate to prevent a nominally estimable matched-date contrast from being mistaken for an adequately observed panel. It pools complete matched pairs across all expected group-date cells, reports the worst date, and rejects malformed counts, duplicated dates, inconsistent coverage, invalid thresholds, and missing pre/post periods. Cutoff dates are canonical ISO dates; observations on the cutoff enter the post period.

For a **constructed** roster of two matched groups on 2025-10-01 through 2025-10-03, daily coverage is 1, 0.5, 0. The pre-period pooled coverage for cutoff 2025-10-03 is 3/4 = 0.75; post coverage is 0/2 = 0. Under a threshold of 0.5, the gate rejects the comparison. This is not an estimate from SEC data.

The threshold 0.9 is a **configurable illustrative default**, not an empirically validated acceptance rule. Report threshold sensitivity, balanced and available-case analyses, and attrition by security, exchange, treatment arm and date. A passing gate does not resolve selection bias or validate causal identification. Calendar provenance and market holidays must be independently authenticated; this module does not infer exchange trading days.

## Verification and limitations

A locally executed prototype with equivalent logic passed 10 unittest cases on 2026-11-05. The published source includes the corresponding ten tests. A fresh-checkout run of the published file remains to be performed. No authenticated SEC daily observations or Nasdaq historical treatment snapshots were available for this phase; no empirical coefficients or research figures were produced. The September pretrends and substantial October placebo remain identification warnings. The historical ZIP inventory and licensing review remain incomplete.

## Next empirical gate

Recover and hash original SEC source archives; authenticate security-date-exchange keys, Nasdaq treatment assignments and historical calendar; execute Phase 170 and 171 on the original panel. Then estimate placebo/pretrend contrasts with security/exchange controls, fixed matched rosters, common-date inference, and serial-dependence-aware sensitivity. Do not describe any reform effect as causal without resolving these gates.
