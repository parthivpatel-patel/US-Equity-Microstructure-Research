# Phase 308 — Exact published Phase 307 regression reproduction (2026-11-11)

## Reproduction
Retrieved `scripts/phase307_eligibility.py` and `tests/test_phase307_eligibility.py` from the public GitHub `main` branch at commit `a0f924639ac259b2122d23309e44837c30e8768a` using the connected GitHub service. Copied the returned UTF-8 contents without changes into an isolated Python workspace, preserving `scripts/` and `tests/` paths. Ran:

```sh
python -m unittest discover -s tests -p 'test_phase307_eligibility.py' -v
```

**Observed:** 12 tests executed; 12 passed; 0 failures; runtime 0.001 seconds. This resolves the narrow Phase 307 caveat that its published file contents had not been executed together. This is an isolated reproduction of the two fetched files, **not** a clone or test of the entire repository checkout or full regression suite.

## Limits and research implications
Tests use hard-coded synthetic records. They establish only the behavior exercised by the tests. The validator does not verify that exchange trading calendars, security eligibility intervals, security identifiers, or SEC panel observations originate from authoritative sources. It does not establish that the reform changed hidden-order execution.

Potential input-contract concerns not yet resolved: an empty supplied session calendar is accepted, as is an empty eligibility universe; neither outcome by itself establishes a valid study sample. The validator reports `empty_intervals` rather than failing on them. Missing rows are not zero-volume observations.

The substantial October 2025 placebo warning, September pretrends, treatment-roster authentication, weighting/selection sensitivity, security and exchange controls, matched-group/common-date and serial-dependence-aware inference remain open. No empirical SEC panel was analyzed here.

## Archive inventory status
Historical recovered ZIPs, manuscript versions, charts, and raw data have not been authenticated or imported in this session. A complete file-level inventory and redistribution-rights review remain outstanding. Do not present those artifacts as published.

## Next gate
Authenticate original SEC source files, their digests and schemas; authenticate trading sessions and security/exchange eligibility; then run September and October placebo/pretrend analyses before interpreting November. The November 14 publication target remains conditional; no causal finding is established.
