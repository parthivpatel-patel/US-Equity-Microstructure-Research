# Phase 360 — Historical eligibility metadata gate (2026-11-14)

Phase 359 accepts caller-declared eligible exchanges, explicitly marking the policy unauthenticated. This phase adds a fail-closed **metadata-only** evidence gate for each security/date policy key: canonical ISO session date, eligible exchange collection, SHA-256 digest format, nonempty source locator, evidence as-of date no later than the session, and agreement between policy and documented exchange set.

**Important limitation:** a well-formed digest string is not proof that source bytes exist or match it. The script intentionally returns `source_bytes_authenticated=False` and `historical_eligibility_authenticated=False`. The source locator and digest in the deterministic tests are fixtures, not real market evidence. The gate must not be used to reclassify actual exchange cells or assert treatment authentication without independently checking source bytes and historical rules.

Ten deterministic prototype checks passed locally, covering valid metadata, missing evidence, invalid dates, future-dated evidence, policy contradiction, invalid digest, malformed exchange collection, duplicates, missing locator, and order invariance. The uploaded test file is an independently authored equivalent; **the exact GitHub checkout has not yet been executed**. No SEC panel observations, historical ZIPs, or licensed third-party records were imported.

**Publication deadline:** November 14, 2026 target not met. September pretrends, October placebo warning, 78 original dated placebo observations, Phase 130 contradiction, selection/weighting sensitivity, source authentication, and calibrated group/common-date/serial inference remain open. No causal effect is established.

**Next:** retrieve and hash original source bytes, reconcile dated security/exchange applicability and round-lot assignments, execute repository-wide tests, then reconstruct placebo and pretrend panels. Historical archive inventory remains incomplete.
