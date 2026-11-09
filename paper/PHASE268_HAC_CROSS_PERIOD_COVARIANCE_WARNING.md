# Phase 268: HAC cross-period covariance warning

Date: 2026-11-09. This note is a mathematical/software audit, **not historical SEC inference**.

For a post-minus-pre estimator, Var(post mean - pre mean) = Var(post mean) + Var(pre mean) - 2 Cov(post mean, pre mean). Applying separate Newey-West estimates to each segment and adding their variances implicitly sets the cross-period covariance to zero. This assumption is not automatically justified for adjacent periods in a serially correlated daily series. Depending on the covariance sign, this may overstate or understate uncertainty.

The included Python routine deliberately labels its result `se_zero_cross_period_covariance`, exposes `cross_period_covariance_modeled=False`, and refuses historical inference authorization. Bartlett weights and sample-autocovariance denominators are documented in source. Nine synthetic tests were run locally after correction of an erroneous hand-calculated lag-one test expectation. No authenticated exchange calendar, matched roster, historical SEC files, or treatment assignments were available for estimation in this session.

Next: derive an influence-function HAC estimator on the **entire** common-date series with period-specific regression regressors, or fit the date-level step regression with a robust full-series sandwich covariance. Evaluate lag and bandwidth sensitivity, small-sample performance, September pretrends, and October placebo dates. Do not interpret any post coefficient causally without source and treatment authentication and satisfactory falsification tests.

Unpublished historical archives, Phase 252–254 implementations, original source manifests, and authenticated treatment roster remain outstanding. No historical coefficients or figures are claimed.
