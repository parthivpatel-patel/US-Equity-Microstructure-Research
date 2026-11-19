# Phase 474 — Exact common-date shock benchmark (synthetic)

**Status:** deterministic model check only; not an SEC-data result or a causal estimate. Date: 2026-11-19.

## Model and estimand

For each of G independent matched groups and T dates, let the balanced-panel outcome under the null be Y[g,t] = a[g] + d[t] + e[g,t], with mutually independent zero-mean components. The time-invariant group component a[g] may have any finite variance. The common-date component d[t] has variance sigma_d squared, and the idiosyncratic component e[g,t] has variance sigma_e squared. All date components are independent across dates in this benchmark. The estimator is the average across groups of the post-minus-pre contrast at each placebo cutoff k. Its date weight is -1/k before k and +1/(T-k) afterward.

The exact covariance between placebo contrasts k and l is

Cov(theta_k,theta_l) = (sigma_d^2 + sigma_e^2/G) sum_t w[k,t] w[l,t].

The group intercept cancels algebraically. Common-date shocks do not diversify away when more matched groups are added. This is an intentionally simplified balanced design; actual treatment-control contrasts may cancel some common-date components depending on their loadings and composition.

## Reproducible constructed example

Using T=40, G=68, cutoffs 10,20,30, sigma_d=sigma_e=1, the exact contrast variances are 0.135294117647, 0.101470588235, 0.135294117647. Omitting the common-date shock would instead give 0.001960784314, 0.001470588235, 0.001960784314. Standard errors are therefore inflated by sqrt(69) = 8.306623863 in this **chosen synthetic model**, not in the SEC data. These numbers are not estimated correlations or empirical effects.

The example is a stress test of a mistaken independence assumption, not evidence that the empirical study has this variance ratio. Group counts are illustrative and do not authenticate the 68-stock treatment cohort. The benchmark does not model serially correlated dates, exchange clustering, heterogeneous factor loadings, group matching, or security selection. In a real DiD, additive shocks shared identically between treated and control securities can cancel; applying this benchmark directly would be inappropriate.

## Reproduction and safeguards

Run `PYTHONPATH=scripts python -m unittest -v tests/test_phase474_two_way_shocks.py` from the repository root. The module uses only the Python standard library. Eight tests check exact formulas, symmetry, group-intercept cancellation, diversification, and invalid inputs. The full repository suite was not run.

## Empirical blockers

Do not certify publication or interpret causal effects until authenticated SEC source files and provenance, round-lot treatment assignment, September pretrends, the substantial October placebo warning, security/exchange controls, weighting and selection sensitivity, and matched-group/common-date/serially dependent inference are resolved. Recovered historical ZIPs and the unpublished Phase 472 executable artifacts were not imported in this phase. The November 14, 2026 target was missed.
