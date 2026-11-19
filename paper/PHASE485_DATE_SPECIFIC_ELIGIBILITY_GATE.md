# Phase 485 — Date-specific eligibility audit and publication gate

**Date:** 2026-11-19. **Scope:** constructed-fixture methodological verification only. No historical SEC observations were accessed or authenticated.

## Research finding

Phase 484 uses a fixed security-exchange universe multiplied by a trading calendar. That denominator may count dates on which a security-exchange unit was not eligible. The proper conditional coverage denominator is the independently authenticated set of eligible (security, exchange, date) keys, not the Cartesian product of a fixed roster and all dates. Let E be the set of eligible keys and O the set of observed panel keys. A valid coverage audit requires O to be a subset of E and no duplicate keys. Missing eligible observations are |E minus O|. Observed zero-valued rows are elements of O and must never be substituted for missing keys.

A local Python prototype, retained in the session workspace, implemented strict CSV schemas, ISO-date calendar checks, duplicate eligibility and observation detection, rejection of observations outside E, finite-outcome checks, daily eligible/observed/missing counts, complete-eligible-unit counts, and SHA-256 file fingerprints. Eight deterministic unit tests passed locally. This commit publishes the methodological report, **not** the prototype or its test suite; therefore no claim is made that the executable is available in the repository.

Constructed fixture: dates 2025-10-01 and 2025-10-02; eligible keys A/X on both dates and B/Y on October 2 only; observed A/X on October 1 with value zero and B/Y on October 2 with value two. The verified prototype returned 3 eligible cells, 2 observed, 1 missing, 1 observed zero, and 1 fully observed eligible unit. These are fixture counts, not SEC estimates.

## Critical provenance caveat

SHA-256 detects changes in supplied bytes but does not establish their SEC origin, licensing, eligibility, completeness, or accuracy. The eligible-key file must be independently sourced, dated, documented, and reconciled with exchange participation and listing/trading rules before historical analysis. No missing observations may be recoded to zero without authenticated evidence.

## Remaining identification blockers

The November 14, 2026 target was missed. The paper is **not publication-certified**. September pretrends, the substantial October 2025 placebo warning, round-lot treatment authentication, selection/weighting sensitivity, security/exchange controls, and matched-group plus common-date and serial-dependence-aware empirical inference remain unresolved. Previously recovered Phase 430/436 archives and Phase 472 executable artifacts remain unimported and unverified in this session.

## Next actions

Publish the tested executable and its regression suite from the retained local workspace after exact-file verification; authenticate source-specific security-exchange-date eligibility and trading calendar; run the coverage gate on licensed, authenticated historical SEC observations; compare fixed and date-varying eligibility denominators and balanced/unbalanced placebo estimates. No causal interpretation is warranted until these checks are satisfied.
