# Phase 374: Exact aggregation and weighting sensitivity

Status: methodological verification only; **no authenticated SEC observations processed**.

## Question
Pooled hidden-execution ratios and equal-row averages estimate different quantities. For rows i with hidden count h_i and total count n_i, the pooled count ratio is sum(h_i)/sum(n_i), whereas the equal-row mean is mean(h_i/n_i). The same distinction applies to share volume. A row may be a security-date-exchange observation, so an equal-row average implicitly weights such observations equally, not securities equally.

## Deterministic counterexample
Two constructed rows with (hidden,total) pairs (1,1) and (0,9) yield a pooled ratio of 0.1 and an equal-row ratio of 0.5. This is **not a market observation**. The gap demonstrates that denominator weighting can change a reported magnitude without any change in source records. It does not imply a sign reversal in the actual reform panel.

## Verification
Seven local unittest cases passed on 2026-11-14, covering the weighting counterexample, exact large integers, empty input, zero denominators, numerator violations, fractional counts, and NaN. Run from the repository root:

```sh
PYTHONPATH=scripts python -m unittest discover -s tests -p 'test_phase374_weighting_identity.py' -v
```

The script intentionally rejects zero-denominator rows instead of selecting an implicit missing-data policy. It uses Decimal arithmetic for exact integer inputs, although resulting ratios are represented at the active decimal precision.

## Empirical requirements still unmet
Before applying this to the historical panel, authenticate original SEC bytes and field definitions, document treatment assignments and cohort selection, check the September pretrends and substantial October placebo, recover the original 78 dated placebo observations, and estimate uncertainty under matched-security and common-date dependence with serial correlation. Report pooled and equal-row estimands separately, with an explicit policy for zero denominators. Do not infer causality from either.

## Archive inventory status
Historical recovered ZIPs and original dated placebo outputs were not accessible or imported in this phase. No third-party raw data were published. Repository-wide integration tests and exact published-checkout tests remain pending. The November 14 publication deadline was missed; manuscript is uncertified.
