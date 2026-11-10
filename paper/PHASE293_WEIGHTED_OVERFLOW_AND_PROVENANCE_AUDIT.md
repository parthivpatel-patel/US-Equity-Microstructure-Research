# Phase 293 — Weighted arithmetic and provenance admission audit

Date: 2026-11-10. Scope: static inspection of published Phase 289 and Phase 292 Python source, plus a direct Python arithmetic reproduction. No historical SEC observations were analyzed.

## Verified defect: finite cells can yield a nonfinite statistic

Phase 289 checks that each exchange contrast is finite, but then calculates `sum(w * by[e] for w, e in zip(weights, exchanges)) / denominator` without checking the resulting daily aggregate. In IEEE-754 binary64 arithmetic, `(1e308 + 1e308) / 2` evaluates to positive infinity despite both inputs being finite. With two exchanges each having one matched pair and both contrasts equal to `1e308`, the pair-weighted daily aggregate can therefore become infinite. A two-date panel can propagate infinity into the returned mean and bootstrap interval without triggering the existing cell-level checks. This is a numerical safety issue, not a claim about realistic SEC data values.

The same issue can arise in the `exchange` weighting mode, and products `w * by[e]` may overflow before aggregation. Proposed correction: use numerically stable normalized weights and `math.fsum` where possible, and reject any nonfinite weighted daily aggregate, returned mean, bootstrap draw, or interval endpoint. Regression tests should exercise overflow, extreme cancellation, and ordinary bounded data under both weighting schemes. Do not infer that `fsum` alone prevents overflow in all weighted products.

## Provenance boundary

Phase 292 requires `source_authenticated is False` and compares observations against a **caller-supplied** calendar. It validates syntax and exact agreement with that calendar but cannot authenticate the calendar's publisher. Phase 289 likewise only accepts `source_authenticated is False`. Accordingly, this pipeline cannot yet be represented as authenticated historical SEC inference. An independent source-manifest verification and a separately authenticated treatment/round-lot roster are required before historical estimates can be reported as authenticated.

## Evidence and limits

Inspected published source paths: `scripts/phase289_common_date_block_bootstrap.py` and `scripts/phase292_calendar_gate.py`. Independently reproduced the Python arithmetic expression `(1e308 + 1e308) / 2`, yielding `inf`, with `math.isfinite` returning `False`. No full repository test run, historical analysis, or patch integration was completed in this phase.

The substantial October 2025 placebo warning, September pretrends, selection/weighting sensitivity, security/exchange controls, and hierarchical matched-security plus common-date serial-dependence-aware inference remain open. No causal effect has been established.

## Next action

Add fail-closed post-aggregation numerical guards to the estimator with deterministic regression tests; rerun the published checkout. Prioritize retrieval and authentication of historical SEC data, exchange calendars, and treatment assignments. Maintain a separate archive inventory; recovered ZIPs remain unverified and unpublished.
