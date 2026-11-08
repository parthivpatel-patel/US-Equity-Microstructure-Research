# Phase 228 — Exact published dependency integration and calendar gap

Date: 2026-11-07. Scope: independent U.S. equity round-lot reform research. **No historical SEC observations were analyzed.**

## Source and reproducibility

Retrieved the UTF-8 contents of these four files from the connected GitHub repository, default branch, before running the tests:

- `scripts/phase224_common_date_hac.py` (blob SHA `591bd0ffd482a647f7b152d13f1bcbf39b308e54`)
- `scripts/phase225_matched_date_bootstrap.py` (blob SHA `f7f5eb4d5e8938a3b9b0f77bdc2638bfd597e6ed`)
- `scripts/phase226_matched_hac_bridge.py` (blob SHA `42d6b8009af898d0dbfd22d5fc57668a376dfaee`)
- `tests/test_phase226_matched_hac_bridge.py` (blob SHA `c1a21804a63fb29efbf949603bf8b52bd9508ba3`)

Copied the retrieved source text into an isolated temporary local directory, preserving the code, and ran:

```bash
PYTHONPATH=<temporary-directory>/scripts python -m unittest discover -s <temporary-directory>/tests -v
```

**Result: 10 tests passed** (seven existing Phase 226 integration tests and three new Phase 228 characterization tests). This is a local execution of reconstructed files fetched directly from GitHub, **not** a clean Git checkout: DNS resolution of github.com failed in the execution container. Python source text was obtained via the connected GitHub API. No historical data were loaded.

## Reproducible calendar defect

`matched_daily` in Phase 225 checks ISO date validity, uniqueness, sorting, and pre-reform date bounds. It does **not** check actual exchange sessions. The Phase 226 bridge does not add such a check. New passing characterization tests demonstrate that the bridge currently **accepts** both:

1. September 6–7, 2025 (Saturday and Sunday) as supposed trading sessions.
2. September 1, 2025 (U.S. Labor Day) as a supposed trading session.

The tests explicitly assert `calendar_authenticated == False`. These are **documented acceptance defects**, not successful calendar-validation tests. The third test confirms ordinary weekday input remains accepted.

## Implication

The estimator can produce numerically well-formed descriptive contrasts and HAC standard errors for a calendar-invalid synthetic panel. Consequently, Phase 226 must not be treated as an authenticated historical estimator until an independently verified exchange-session gate is wired into its input path and covered by rejecting regression tests. A weekday-only gate is insufficient because it would still admit Labor Day.

## Historical identification status

The substantial October 2025 placebo warning, September pretrends, Nasdaq historical round-lot classification, original SEC source authentication, weighting sensitivity, matched-roster selection, and security-level uncertainty remain open. There is no established causal effect.

## Archive inventory and publication gap

Previously reported approximately 129 historical research ZIPs (approximately 1.16 GB total) were **not available to inspect in this session**. No file-level complete inventory or redistribution-license determination can be certified. No archives, historical SEC records, manuscript figures, or empirical coefficients were imported. The exact missing-file list is therefore **unknown**, not zero.

## Next action

Implement an independently sourced session calendar with explicit provenance and strict failure on missing/invalid sessions, then rerun the exact Phase 226 bridge tests and evaluate September/October placebo contrasts only after historical SEC panel and treatment labels are authenticated.
