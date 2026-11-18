# Phase 461 — Observed matched-date placebo overlap

This diagnostic extends Phase 460's calendar-only overlap calculation to **observed, paired exchange–matched-group dates**. It counts dates with both treated and control observations, screens each placebo cutoff for minimum pre/post support, and measures which observed dates switch placebo-period labels between cutoffs. Pairwise comparisons are restricted to groups eligible at both cutoffs. No observations are imputed.

## Interpretation and limitations

The observed date count is **not** a count of independent observations: common market dates and shared securities induce dependence. Pairwise eligibility can change with the cutoff; the intersection of eligible groups across all cutoffs is also reported. The diagnostic does not estimate treatment effects, authenticate data or treatment, perform serial-dependence-aware inference, or resolve September pretrends and the substantial October 2025 placebo warning.

Constructed six-date fixture: under minimum one pre-date and two post-dates, September 1 and October 1 cutoffs share one eligible group; two observed dates are reassigned from post to pre. Under the default two-pre-date requirement, the September 1 cutoff is ineligible. These are synthetic software-test facts, **not SEC data**.

Run locally: `cd scripts && PYTHONPATH=. python -m unittest discover -s ../tests -p 'test_phase461_observed_overlap.py'`. Eight deterministic tests passed in the development environment on November 18, 2026. The complete repository regression suite and the exact published checkout have not been executed.

## Research gate

Do not present placebo comparisons as independent replications or causal evidence. Before empirical reporting, authenticate SEC source files and historical round-lot assignments, audit trading-session calendars and missingness, evaluate September trends and October placebos, compare weighting/support estimands, and use common-date plus serial-dependence-aware inference. Historical recovered archives and Phase 430/436 prototypes were not imported in this phase.
