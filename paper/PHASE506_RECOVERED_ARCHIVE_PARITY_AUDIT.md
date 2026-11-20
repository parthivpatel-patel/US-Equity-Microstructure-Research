# Phase 506 — Recovered archive-to-publication parity audit

Date: 2026-11-20. **Executable reproducibility verification; not historical SEC inference.**

## Directly verified evidence

The retained `phase504_validation.zip` was extracted in an isolated local directory. Its 11 Phase 504 tests were run with `python -m pytest -q phase504/test_phase504_support_attrition.py`: **11 passed in 0.05 seconds**. This is a run of the recovered ZIP's files, not an independent checkout of GitHub.

Git blob hashes calculated with `git hash-object` for the extracted source and test were compared with the GitHub connector's live `fetch_file` blob SHA values on the existing public default branch:

| Artifact | Recovered ZIP Git blob SHA | GitHub blob SHA | Result |
|---|---|---|---|
| `scripts/phase504_support_attrition.py` | `91df354d6c9a053b97807d4100bbc4261ae2892d` | `91df354d6c9a053b97807d4100bbc4261ae2892d` | Exact byte parity |
| `tests/test_phase504_support_attrition.py` | `fff6a9c5bf653add4da2e7ab15d7154d21d56814` | `fff6a9c5bf653add4da2e7ab15d7154d21d56814` | Exact byte parity |

SHA-256 checksums of the recovered archive entries (not source-data authentication): source `13ce44436de02f2137d0c8216bca797c72b130513a3b8aaa29d439e35c8bab7f`; tests `4a7de4fc45307b76a5178bb63aec655409036b0cbac1467948bebc83c7ad9340`; report `ddfc5c187c1259ac35002db4c44027caf2993d56a0d095893a4d065c87dc736b`.

The recovered ZIP report and the public Phase 504 report have different Git blob hashes (`895b18378a02d93079c81ad3ba0604d8d4709df7` for ZIP versus `0cc768af8296a4ac9ebbf6c567604b29ce4be768` for public). Therefore **report byte parity is not established**. The public report was read before this audit; it documents the earlier executable-publication gap, which Phase 505 subsequently closed. Do not overwrite that historical record.

## Interpretation and remaining design risks

This closes the narrow question of whether the recovered Phase 504 executable and tests match the current public files, with a passing local fixture run. It does **not** prove that a fresh GitHub checkout runs successfully, or that any historical SEC observation, eligible-security roster, exchange mapping, matched group, round-lot assignment, calendar, or placebo estimate is authentic.

Phase 504 groups on exchange and the pre/post reform cutoff and measures eligibility-based common-date support. It does not independently authenticate trading sessions, security-level matching, serial correlation, or source provenance. An eligible date with zero observed units still counts as common eligibility support, by design. No causal effect can be inferred from these coverage statistics.

## Publication gates and next analysis

1. Acquire and hash the actual SEC source files and date-specific round-lot eligibility evidence; preserve download URLs, retrieval timestamps, schema, and permissions.
2. Reconcile the historical security-date-exchange keys and matched treatment/control membership; reject duplicates and unexpected calendar days.
3. Execute Phases 496–504 on authenticated September and October observations and report attrition by exchange, group, and date.
4. Revisit the substantial October 2025 placebo and September pretrends using common-date matched-group estimands and security/exchange controls; use date-clustered or block/bootstrap inference appropriate to temporal dependence.
5. Inventory and validate Phase 430/436 ZIPs and Phase 472 materials before importing any redistributable artifacts.

**Deadline status:** The November 14, 2026 target has passed. The manuscript remains **not publication-certified**. This report contains no empirical reform-effect estimate.
