# Phase 502: calendar-date and period-label integrity

**Status:** deterministic fixture validation only; no authenticated historical SEC observations.

## Finding

The existing Phase 501 aggregation accepts arbitrary nonempty date strings and trusts caller-supplied `pre` and `post` labels. Thus an observation dated after the cutoff can be incorrectly grouped into the pre-period without triggering the aggregation's existing validation. This is an input-admission limitation, not evidence that the historical panel contains such errors.

## New guard

`scripts/phase502_period_integrity.py` validates strict ISO `YYYY-MM-DD` calendar dates, rejects mislabeled period rows relative to a caller-selected cutoff (default November 3, 2025), rejects explicitly excluded dates, and returns copies of admitted records. The cutoff day is classified as post. It intentionally does **not** infer exchange trading calendars, authenticate source data, verify round-lot assignments, or estimate any effects.

Run: `PYTHONPATH=scripts python -m pytest -q tests/test_phase502_period_integrity.py`.

Local fixture validation: **11 tests passed** (2026-11-20); the exact remote checkout has not been rerun.

## Implications for historical analysis

Validate cutoff and period labeling before Phase 501 coverage aggregation, September pretrend work, October placebo comparisons, and any DiD inference. Obtain an authenticated trading calendar before interpreting missing dates as missing observations. The substantial October placebo warning, treatment authentication, security/exchange selection, weighting sensitivity, and common-date/serial dependence requirements remain unresolved. No causal inference is warranted.

## Historical artifact inventory

Phase 430/436 recovered ZIPs and Phase 472 artifacts are reported as not yet imported or source-verified. This phase did not inspect or redistribute them.

**Publication status:** November 14, 2026 target missed; paper not publication-certified.
