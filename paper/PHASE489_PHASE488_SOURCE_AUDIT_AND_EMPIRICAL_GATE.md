# Phase 489 — Published-code source audit and empirical admission gate

Date: 2026-11-19. Scope: independent November 3, 2025 U.S. equity round-lot reform research.

## Materials inspected
- `scripts/phase488_period_composition.py` on the public default branch (blob `04caad64eff0ce29bc901cde2bf81ec90870be1c`).
- `tests/test_phase488_period_composition.py` on the public default branch (blob `644a2a80ddcfa7ff391b40f26ef1b0b919afdc66`).

This is a **static source review**, not an execution of the published checkout or an empirical analysis of SEC data. Do not treat the nine published tests as independently rerun.

## Confirmed behavior from inspection

1. The auditor treats an explicitly recorded zero as observed, because membership in the observation dictionary is distinct from the numeric outcome.
2. It rejects duplicate keys, nonfinite outcomes, out-of-universe observations, and cutoff dates without eligible cells on both sides.
3. It computes eligibility and observed-unit composition separately and reports missing cells by exchange.
4. Its SHA-256 hashes attest only to the bytes supplied to the program; they **do not authenticate** the upstream SEC publisher, security identifiers, eligibility definition, treatment status, or redistribution rights.

## Newly identified edge cases / open defects

- **Malformed CSV width:** `csv.DictReader` may put surplus fields under the `None` key as a list. The expression `v.strip()` can then raise `AttributeError` instead of a controlled `ValueError`. A short row can also produce `None` values (which are rejected). A dedicated malformed-row regression test is needed.
- **Whitespace normalization:** nonblank security/exchange identifiers are not stripped before key construction. A value `'A '` is a different unit from `'A'`; this is a deliberate raw-byte distinction unless an authenticated normalization policy is specified.
- **Calendar admission:** the eligibility CSV is accepted as a claimed set of dates; the program does not verify NYSE/Nasdaq trading sessions, half-days, security-specific listing status, exchange reporting eligibility, or corporate-action identifier continuity.
- **Temporal composition:** `both` means a unit appears at least once in each period, not that it has complete coverage in either period. It must not be labeled a balanced panel.
- **Selection:** conditioning on complete units can induce selection bias. Coverage is a diagnostic, not a sufficient identification repair.

## Empirical protocol (not yet executed)

Let `E_itx` denote independently authenticated eligibility for security `i`, date `t`, exchange `x`, and `O_itx` denote whether an observation exists. Define period coverage as

`C(P) = sum_{(i,t,x) in P} E_itx O_itx / sum_{(i,t,x) in P} E_itx`.

This denominator must be computed from independently sourced eligibility, **not** reconstructed from observed panel rows. Report it for September pretrends, the October placebo window, and the November reform window, separately by treatment cohort, matched group, and exchange. Distinguish structural noneligibility from missing eligible observations and observed zero outcomes.

For each cutoff, retain a stable pre-specified matched-group weighting rule, report both all-eligible and fixed-composition estimates where identifiable, and quantify coverage differences by group. Placebo dates should be pre-specified, not selected by smallest p-value. Use joint matched-group and common-date resampling with dependence-aware time blocks or an explicitly justified alternative; naive independent row bootstrap is inadmissible. Record finite-sample cluster counts and sensitivity to block length.

**Stop gate:** Do not interpret October placebo, September trends, or November coefficients causally until source file URLs, retrieval dates, publisher provenance, checksums, exchange/security mapping, round-lot treatment history, eligible-date calendar, and redistribution permissions are independently documented. If the historical panel is unavailable, record this as blocked rather than substituting synthetic data.

## Backlog and publication status

- Phase 488 exact published checkout: targeted execution pending.
- Phase 489 malformed-width regression and controlled error handling: pending implementation.
- Authenticated SEC historical panel and date-specific eligible universe: pending.
- October placebo and September pretrend re-estimation: pending.
- Phase 430/436 recovered ZIPs and Phase 472 executable archive: inventory/import pending, with license and file-size review.
- November 14, 2026 manuscript deadline: missed; paper **not publication-certified**.

No empirical statistics or causal conclusions are introduced in this note.
