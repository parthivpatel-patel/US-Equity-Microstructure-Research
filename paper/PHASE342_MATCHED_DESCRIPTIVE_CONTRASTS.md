# Phase 342 — Paired descriptive contrasts with exchange support (2026-11-13)

This standard-library script extends Phase 341's support audit to **descriptive** numerator/denominator contrasts within match-group × calendar-date × exchange cells. It excludes cells missing either arm. Each arm's numerator is summed before division by its summed denominator; the treated-minus-control difference is expressed in percentage points. The final summary equally weights matched groups, first averaging paired cells within each group. This is not equivalent to a trade-weighted, security-weighted, or calendar-date-balanced estimand.

**Critical scope limitation:** No authenticated SEC source panel was available in this session. The ten tests use constructed fixtures only. No empirical treatment effects, confidence intervals, placebo results or causal claims are produced. The script explicitly labels authentication false and inference not computed. Cross-group/date/exchange dependence, serial correlation, staggered sample availability, and selection effects remain unaddressed.

**Validation:** Ten deterministic local tests passed on the same algorithm before publication, including ratio-of-sums, equal group weighting, missing exchange overlap, duplicates, assignment drift, zero denominators, impossible numerator values, empty data and malformed dates. Exact post-publication checkout execution and complete suite are outstanding.

**Reproduction:** From repository root: `PYTHONPATH=scripts python -m unittest discover -s tests -p 'test_phase342_matched_contrasts.py' -v`; `python scripts/phase342_matched_contrasts.py AUTHORIZED_PANEL.csv`. Required fields: security,date,exchange,treated,match_group,numerator,denominator. Input must be licensed for local use; do not publish restricted raw observations.

**Publication gate:** Phase 130 five-day placebo-count contradiction, 78 original dated placebo observations, September pretrends, October structural break, cohort authentication, source provenance, matched/common-date dependence-aware inference, selection/weighting sensitivity, and historical ZIP provenance remain unresolved. November 14 publication certification is not justified.

**Next:** Locate authenticated dated placebo and panel sources, run Phases 340–342 jointly, compare equal-group against alternative weighting schemes, then implement common-date plus group-block resampling with explicit effective-sample diagnostics. No GIG code or assets used.
