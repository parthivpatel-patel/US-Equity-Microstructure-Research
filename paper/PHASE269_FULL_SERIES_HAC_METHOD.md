# Phase 269: full-series HAC diagnostic (9 November 2026)

This is a **software and methodology artifact**, not an empirical finding. It corrects a limitation flagged in Phase 268: separate pre/post HAC calculations omit lagged covariance across the cutoff.

For each date, compute the equal-weight mean treated-minus-control contrast across observed matched pairs. Regress this daily contrast on an intercept and a post-cutoff indicator. Let n0 and n1 be pre/post date counts, and let e_t be the fitted residual. The exact OLS contrast influence is z_t = e_t*(post_t/n1 - pre_t/n0). The Bartlett HAC variance is sum(z_t^2) + 2 sum over lags k=1..L of [1-k/(L+1)] sum over t>k of z_t*z_(t-k). This includes lagged products spanning the reform cutoff. No finite-sample correction is applied.

Run: `python -m unittest tests.test_phase269_full_series_hac`. For a CSV with columns date,pair,treated,control, run `python scripts/phase269_full_series_hac.py --csv YOUR_FILE.csv --cutoff 2025-11-03 --lag 3`.

**Critical limitations:** The program enforces a consistent *observed* pair roster but does not authenticate a predetermined treatment roster, source files, SEC field definitions, exchange trading calendar, missing entire pairs, or market-wide confounders. It does not fit security/exchange fixed effects, adjust for multiple comparisons, validate September pretrends, resolve the substantial October placebo warning, or establish causality. HAC asymptotics can be unreliable with few trading dates and strong dependence. Lag selection must be disclosed and varied. Date-level aggregation does not by itself resolve selection or security-level dependence.

Historical SEC input and treatment authentication remain outstanding. No historical estimate, chart, causal effect, or publication-ready result is claimed. Previously recovered ZIP archives and unpublished Phase 252–254 artifacts have not been authenticated or imported. Next: authenticate raw SEC downloads and official round-lot assignments, lock roster and calendar, run historical pretrends/placebos and compare HAC lag choices with block/bootstrap sensitivity.
