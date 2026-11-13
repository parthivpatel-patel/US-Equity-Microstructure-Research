# Phase 327 — Cross-outcome historical placebo-window provenance gate (2026-11-13 UTC)

## Why this check matters

The published Phase 130 aggregate summary reports 78 placebo windows for hidden-execution count and volume. Equal window counts **do not prove** the outcomes were computed over the same dated windows. This matters especially because the count row's negative-tail, absolute-extreme, and maximum statistics are jointly inconsistent under the documented common-population definitions (Phase 322).

## New verification

The accompanying standard-library script accepts the dated placebo CSV format specified by Phase 325, checks unique (outcome, window_id) identities, ISO intervals ending before the November 3 reform, and finite decimal estimates. It compares window IDs and start/end dates across each outcome pair, identifying missing or mismatched windows. Distinct outcome-specific filters can be legitimate; discrepancies are diagnostic and must be traced to the summary producer rather than automatically treated as errors.

Eight deterministic synthetic tests passed locally on 2026-11-13 UTC. They cover matching identities, missing identities, mismatched intervals, duplicate IDs, nonfinite values, post-reform intervals, reversed dates, and empty inputs. No original SEC observations or 78 dated placebo-window values were available for this test. Accordingly **no empirical window-alignment conclusion is claimed**.

## Reproduce

From repository root:

```bash
python -m unittest discover -s tests -p 'test_phase327_cross_outcome_audit.py' -v
python scripts/phase327_cross_outcome_audit.py PATH_TO_AUTHENTICATED_DATED_WINDOWS.csv
```

## Publication gate and next step

Do not interpret overlapping placebo frequencies as independent p-values, and do not repair the Phase 130 count contradiction by altering the aggregate CSV without tracing its producer. Recover original window-level output and source manifests, then run Phases 325–327 jointly. Historical treatment assignments, September pretrends, October placebo warning, security/exchange effects, selection/weighting sensitivity, and common-date/serial-dependence-aware inference remain unresolved. Historical ZIP files and redistribution rights have not been authenticated. November 14 is a target, not a certification.
