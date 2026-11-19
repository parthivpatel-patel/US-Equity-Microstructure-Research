# Phase 466: Joint placebo bootstrap eligibility dependence

## Scope
This phase extends the Phase 465 exact support enumeration by calculating pairwise joint eligibility, covariance of eligibility indicators, and conditional eligibility probabilities for overlapping placebo cutoffs. It enumerates all equally likely moving-block start sequences, truncating concatenated blocks to the original session count. It does not use historical SEC outcomes.

## Deterministic verification
Six consecutive illustrative dates, block length three, two independently sampled block starts (four possibilities each) yield 16 equiprobable paths. Eligibility counts for cutoffs before sessions 1 and 3 are 7 and 14; jointly eligible paths are 6. Therefore the joint probability is 6/16 = 0.375, while the product of marginal eligibility probabilities is (7/16)(14/16) = 0.3828125. Eligibility-indicator covariance is -0.0078125; P(first eligible | second eligible) = 6/14. These are design arithmetic, not empirical market findings. Eight local unittest cases passed on 2026-11-18; the exact published checkout and full repository suite were not executed.

## Interpretation
Shared resampling paths induce joint support selection. Conditional acceptance of all placebo cutoffs can change the distribution of retained paths. Eligibility covariance is NOT the covariance of estimated placebo effects, and its sign says nothing about the latter. Exact enumeration scales exponentially and is limited by max_paths. Real exchange calendars, matched groups, missing observations, treatment assignments and historical data provenance remain unauthenticated. This is not null-centered simultaneous inference or a causal test.

## Publication gate
The November 14, 2026 deadline was missed. Historical September pretrends and the substantial October placebo warning remain unresolved, as do source-data and treatment authentication, weighting and sample-selection sensitivity, dependence-aware empirical inference and historical ZIP recovery. Do not interpret any constructed test numbers as SEC estimates.

## Reproduction
From repository root: `PYTHONPATH=scripts python -m unittest discover -s tests -p 'test_phase466_support_dependence.py' -v`.
