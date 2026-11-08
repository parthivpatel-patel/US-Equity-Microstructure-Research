# Phase 245 — Phase 244 dependency-chain execution audit

Date: 2026-11-08. Scope: synthetic software verification only; no historical SEC observations.

## Source provenance
Read the default-branch contents of `scripts/phase224_common_date_hac.py`, `scripts/phase242_placebo_scan.py`, `scripts/phase243_placebo_calendar_guard.py`, `scripts/phase244_guarded_placebo.py`, and `tests/test_phase244_guarded_placebo.py` using the connected GitHub read service before testing. The local test directory contained manually transcribed source from these retrieved files, not a Git clone or independently authenticated checkout. The transcriptions were not byte-for-byte checked against the GitHub blobs, so this is **not** an exact-repository test-suite execution. No production files were changed.

## Execution
Command: `PYTHONPATH=/mnt/data/phase245/scripts python -m unittest discover -s /mnt/data/phase245/tests -v`.

Observed: **7 tests ran; 7 passed; 0 failures/errors**, in the locally transcribed four-module dependency chain. Cases: known linear synthetic contrast, weekend rejection, holiday nonauthentication, roster mismatch, duplicate dates, incomplete windows, and NaN rejection. The six dated synthetic observations are September 29–October 6, 2025 (regular weekdays); a holiday test intentionally substitutes September 1. The fixture's equal-cell difference was 3 and pooled-count difference 6; these are synthetic test numbers, not SEC findings.

## Methodological limits and follow-up
The existing guard checks weekdays, not authoritative exchange closures. Its optional `admitted_sessions` is merely caller supplied. It does not validate treatment assignment, SEC source lineage, missing dates, exchange effects, matched controls, overlapping placebo-cut multiplicity, or security-cluster uncertainty. A caller-supplied roster can itself be wrong. Source and treatment authentication remain false. The October placebo and September pretrends remain major unresolved threats to causal interpretation. No causal effect is established.

Next: execute the exact published test suite in a verified checkout; obtain authenticated SEC input hashes and exchange-session evidence; lock fixed treatment/control rosters before historical September/October placebo and dependence-aware analyses. Historical research archives were not available for authenticated import this session, and no complete archive inventory was verified. Publication target November 14 remains conditional.
