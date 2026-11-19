# Phase 481 — Historical panel coverage audit specification

Date: 2026-11-19. This phase adds a **data-quality instrument**, not a new empirical estimate. No SEC data have been authenticated or included.

The companion standard-library script reads a user-supplied CSV with security, date, exchange, and value columns, optionally source_id. It rejects duplicate security-date-exchange keys, invalid ISO dates, nonfinite values and blank security/exchange keys. It reports explicitly observed zeros separately from absent rows, unique security-exchange units, the fraction of units represented on every **observed** date, and daily coverage relative to the union of observed units. Exchange is part of the unit key to avoid silently merging exchange-specific observations.

**Important limits:** The union of observed units is not an authoritative universe. The observed date list is not an exchange trading calendar. A valid CSV is not proof of SEC provenance. No imputation, treatment authentication, pretrend estimation, or causal inference is performed. Before historical analysis, require source checksums, SEC retrieval records, an independently verified trading calendar, round-lot treatment evidence, and explicit missing-versus-zero policies.

Reproduce: `python scripts/phase481_coverage_audit.py PATH_TO_AUTHENTICATED_PANEL.csv --output coverage.json`; run `python -m unittest discover -s tests -p 'test_phase481_coverage_audit.py' -v`. Five isolated tests passed locally. The full repository suite was not run.

**Publication:** November 14, 2026 target missed; manuscript not publication-certified. September pretrends, substantial October placebo, treatment authentication, selection/weighting sensitivity, and dependence-aware empirical inference remain unresolved. Recovered Phase 430/436 archives and Phase 472 executable artifacts remain unpublished.
