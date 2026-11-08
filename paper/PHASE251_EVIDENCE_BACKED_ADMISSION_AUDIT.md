# Phase 251: Evidence-backed admission audit (2026-11-08)

## Verified code-level finding

Direct inspection of `scripts/phase249_admission_policy.py` and `scripts/phase250_provenance_bridge.py` on the public default branch confirms that the latter accepts four caller-supplied booleans (`source_authenticated`, `calendar_authenticated`, `treatment_authenticated`, `license_authorized`). The code labels their origin `caller_supplied_not_independently_verified`. Neither module checks independent evidence records, authoritative publication identifiers, acquisition timestamps, treatment-rule provenance, or licensing documentation. Consequently, `historical_estimation_allowed=True` is a **conditional software decision**, not independently verified admissibility. This is a source-code audit, not a historical-data finding.

## Required evidence ledger before empirical claims

For each input dataset, record publisher, exact original download URL, publication/version date, retrieval timestamp in UTC, SHA-256 of the exact bytes, file size, original format, transformations and hashes of derived files, and a redistribution decision supported by terms. For exchange sessions, record the authoritative calendar source, its version, closure and half-day treatment, and a hash of the exact session roster. For the affected-security assignment, record the pre-reform price reference, rule thresholds, corporate-action adjustment convention, security identifiers and mapping version, independent verification of each assigned category, and an immutable treatment-roster hash. Explicitly distinguish unverified, verified, and unavailable evidence. A string or boolean assertion alone must not upgrade any item.

## Prespecified empirical gate and design

1. Fail closed if source bytes, session calendar, treatment assignment, or rights are unverified. Rights to **analyze** and rights to **redistribute** must be evaluated separately; lack of redistribution permission does not automatically preclude lawful local analysis.
2. Freeze the security roster and matching rules using pre-event information. Report attrition, unmatched treated units, security/exchange coverage, and weight concentration. Retain both equal-cell and pooled-count estimands rather than switching to the preferred sign.
3. Fit September pretrend diagnostics and prespecified October placebo cutoffs using identical outcomes, samples, controls, weights, and window widths. Report the substantial pre-reform placebo as a threat to identification, not an inconvenience to discard.
4. Include security and exchange controls where identifiable, common-date shocks, and dependence-aware uncertainty. Cluster by security for serial correlation and evaluate common-date dependence with appropriate date-level or two-way clustering where the panel supports it. With few time clusters, explicitly qualify asymptotic inference; use appropriate bootstrap sensitivity rather than treating overlapping placebo windows as independent.
5. Report multiple-testing sensitivity, negative controls, alternate matching, treatment classification perturbations, missingness, outlier exclusions, and outcome denominator sensitivity. Any historical effect estimate remains descriptive until pretrend and placebo objections are resolved.

## Verification and disclosure

This session did **not** retrieve original SEC data, authenticate any roster, run historical regressions, produce empirical statistics, or execute the full repository test suite. No prior research ZIP was available for authenticated import; a complete historical-artifact inventory remains outstanding. No causal effect is established. The November 14 manuscript target is conditional on evidence-backed validation. Next step: replace caller-only attestations with inspectable evidence-ledger entries, then apply the frozen historical design to authenticated inputs.
