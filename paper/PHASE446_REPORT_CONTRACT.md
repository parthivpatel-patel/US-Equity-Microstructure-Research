# Phase 446 — Source-bound report consistency contract

Date: 2026-11-18. Status: structural software validation only; not publication certification.

## Scope and motivation

Read the existing Phase 437, 439, 442, 443, and 445 Python implementations before adding this independent audit. Phase 443 binds assignment checks to the same raw bytes as the daily/calendar pipeline. Phase 445 adjudicates security-only flags separately. The present contract checks whether a combined Phase 443-style report is internally coherent before it is used in later interpretation. It does not modify earlier scripts or relax support gates.

The validator requires matching SHA-256 digests, byte lengths and observation counts in top-level, daily, calendar and assignment reports. It rejects contradictory assignment pass flags and conflict lists, duplicate conflict identifiers, Boolean values masquerading as integer counts, unsupported treatment-authentication claims, and unsupported historical-effect claims. A legitimately failed assignment audit is a *valid report* even though it is not a passing empirical validation. The returned `contract_valid` flag must not be interpreted as the underlying panel's validation status.

## Reproducible local verification

`cd scripts && PYTHONPATH=. python -m unittest discover -s ../tests -p test_phase446_report_contract.py -v`

Ten deterministic unit tests were run in an isolated local directory on 2026-11-18: **10 passed, 0 failed**. The tests construct reports in memory; they do not execute the published repository checkout, its entire test suite, or SEC data. No historical estimates or figures were produced.

## Limitations and publication blockers

This is report-contract validation, not a cryptographic signature from the SEC. A consistent fabricated or wrongly sourced CSV still passes the consistency checks. Source provenance, 2025 round-lot treatment assignments, September pretrends, the substantial October placebo warning, weighting/selection sensitivity, and matched-group/common-date serial-dependence-aware inference remain unresolved. Historical research ZIPs were not available for inspection in this session and none were imported. Phase 430 and Phase 436 prototypes remain outstanding. Do not claim a causal effect.

The November 14, 2026 publication target was missed; the paper remains **not publication-certified**.

## Next task

Run the exact published checkout's tests; wire this contract into the Phase 443 output *without* turning a failed underlying panel into a pass; then prioritize authenticated historical input and prereform falsification before any effect estimation.
