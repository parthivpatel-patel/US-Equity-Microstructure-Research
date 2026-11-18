# Phase 459 — placebo-date grid and stable-support sensitivity

This session extends Phase 458's single October 1 boundary to a grid of pre-reform placebo dates. The diagnostic reports each exchange/matched-group's treated-minus-control difference before versus after each candidate date, using only dates before November 3, 2025. It separately reports estimates using the intersection of eligible groups across all specified placebo dates. This separates changes in estimated placebo effects from changes in eligible matched-group composition.

It rejects duplicate security-exchange-date observations, nonfinite outcomes, changing exchange/group assignments, cross-exchange treatment conflicts, and duplicate placebo boundaries. Unpaired cells are counted, not silently treated as zero. Dates are calendar dates, not authenticated exchange sessions.

Eight deterministic tests passed locally with constructed observations. In the synthetic fixture the October 1 placebo estimate is 3.5; this is **not an SEC observation or an empirical effect**. The grid does not perform serial-dependence-aware inference, authenticate historical treatment, or identify a causal effect. Multiple placebo comparisons should not be read as independent tests.

**Blocking requirements:** SEC source provenance and byte-level manifests, authenticated historical round-lot assignments, September pretrends, substantial historical October placebo warning, weighting sensitivity, and date-block inference. No historical archives imported; Phase 430/436 remain unpublished. November 14, 2026 publication target missed; manuscript not publication-certified.
