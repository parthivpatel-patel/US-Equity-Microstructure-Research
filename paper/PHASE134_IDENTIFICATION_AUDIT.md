# Phase 134 — Identification and event-window audit (November 3, 2026)

## Scope and verification level

This is a **new independent arithmetic and design audit of the published Phase 131 CSV and Phase 133 report**, not a fresh run on authenticated SEC records. The repository's processed 14,416-row input is not public. A separate source-level empirical inference result cannot be claimed.

## Directly checked against published Phase 131 table

| Outcome | November event sign across 3/5/7/10/15-day windows | November minus October 6 sign | Range of November minus October 6 (pp) |
|---|---|---|---|
| Hidden trade count | negative in all 5 | negative in 4, positive at 10 days | -0.734661 to +0.337165 |
| Hidden share volume | negative in 4, positive at 7 days | positive in all 5 | +0.201918 to +1.156684 |

Each of the ten published `nov_minus_oct_pp` values equals `november_pp - october6_pp` within 0.0000011 pp (six-decimal table rounding). This audit checks **internal consistency only**; it does not verify the underlying observations.

The count contrast reverses sign between five and ten trading days. Volume's November **event estimate itself** changes sign at seven days even though the *November minus October* contrast remains positive. Distinguish these estimands in all paper text and figures.

## Identification audit

1. The Phase 133 monthly matched-group contrast series is **not** a test of parallel treated/control trends: treatment/control levels and separate slopes are not available in that public summary. The July–October movements demonstrate instability but cannot identify which side drives it.
2. November's Phase 133 monthly mean combines observations **before and after November 3** and must never be labeled a pure pretrend.
3. October 6's five-day contrast uses September 29–October 10 and includes October 1, a potential information event about future round-lot assignments. It is **not** a clean untreated placebo.
4. The 3/5/7/10/15-day windows and 78/74/etc. historical pseudo-event counts overlap. The empirical ranks are neither independent tests nor valid familywise p-values. Windows and the October comparator were explored post hoc.
5. The equal-weighted 68-group series cannot identify exchange heterogeneity or verify original treatment assignment. Selection and thin-venue complete-case exclusions are not audited.
6. Group-only bootstrap and leave-one-group-out sensitivity cannot capture shared calendar-date shocks or serial dependence. A date-aware design must preserve the joint cross-sectional date shocks and use justified block lengths, with sensitivity analysis. With a **single common policy date**, date-clustered resampling does not magically solve event-time confounding.

## Falsification-first release gate

Before asserting any policy effect: (a) authenticate historical security-specific round-lot assignments and corporate actions, (b) reconcile SEC raw security-by-exchange daily outcomes, (c) freeze treatment/control cohorts, weights, outcomes and event horizons, (d) inspect separate pre-reform treated/control trends and placebo windows, (e) run venue and security heterogeneity plus dependence-aware uncertainty, and (f) disclose specification search and multiplicity. Until then **no causal effect has been established**.

## Reproducibility

Run `python tests/audit_phase134_published_window_table.py` from repository root using Python 3.9+. It reads the existing published CSV, uses only the standard library, asserts the reported relationships and signs, and prints a concise JSON result. No generated or reconstructed observations are used.
