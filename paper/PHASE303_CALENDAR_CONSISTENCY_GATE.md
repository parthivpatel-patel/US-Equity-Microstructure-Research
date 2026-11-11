# Phase 303 — Calendar consistency gate (2026-11-10)

**Status:** validated synthetic software check; no authenticated SEC data examined.

The Phase 289 bootstrap accepts strictly increasing date strings without independently validating calendar provenance. This new standalone gate checks canonical ISO dates, weekdays, ordering, duplicates, and exact coverage against a supplied list of expected dates. It returns missing/extra dates and explicitly sets `calendar_authenticated`, `source_authenticated`, and `causal_inference_authorized` to false. A caller-supplied calendar is **not independently authenticated**; a weekday can still be an exchange holiday (e.g., 2025-09-01). Do not treat a successful consistency check as source authentication or market-session verification.

Seven deterministic tests passed in a local isolated run (0 failures); the exact published checkout has not been separately tested. Run `python -m unittest tests.test_phase303_calendar_gate -v` from repository root. No change to Phase 289's production bootstrap or to historical estimates is claimed.

**Identification and evidence gate:** September pretrends, the substantial October 2025 placebo, provisional treatment rosters, matched-security selection, pair-versus-exchange weighting, security/exchange composition, and joint matched-group/common-date/serial-dependence inference remain unresolved. Original SEC source files, calendar authority and their hashes must be verified before historical estimation. No causal effect is established.

**Archive inventory:** Previously recovered historical ZIPs, manuscript versions, code, and charts have not been authenticated or imported during this session; a complete manifest is not yet available. No third-party datasets or synthetic empirical figures were uploaded.

Next: authenticate the exchange trading-session calendar and original SEC data, build source hashes and roster checks, run published regression tests, and only then perform actual September/October diagnostics.
