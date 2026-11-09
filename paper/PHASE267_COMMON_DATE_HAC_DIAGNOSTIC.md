# Phase 267 — Common-date serial dependence diagnostic

November 9, 2026. Independent quantitative-finance research software; not a historical reform estimate.

The implementation averages treated-minus-control contrasts across a complete fixed pair roster for each common date, then computes the post-minus-pre mean and a Bartlett/Newey–West HAC standard error on residuals from a two-regime intercept-plus-post fit. Date-level averaging retains common-date dependence across matched pairs. HAC permits limited temporal dependence but requires weak dependence and sufficient time observations. The lag heuristic is not guaranteed to yield reliable coverage; no finite-sample correction is applied.

The procedure rejects incomplete date-by-pair panels, duplicate records, nonfinite values, invalid lag settings, and fewer than three dates per period. It does not authenticate exchange calendars, SEC extracts, security/exchange identities, treatment assignments, or matched-pair construction. It does not estimate exchange fixed effects or pretrends and cannot establish causality. Nine deterministic synthetic tests passed locally on an equivalent implementation. A perfect synthetic step yielded a contrast of 2 and zero residual-based standard error, which must not be interpreted as empirical precision. The exact published files were not independently rerun after publication.

No authenticated historical SEC observations, historical coefficients, or figures were produced. September pretrends, the substantial October placebo warning, treatment authentication, selection and weighting sensitivity, and serial dependence remain unresolved. Recovered historical ZIPs and unpublished Phase 252–254 artifacts were not available for import; the complete historical archive inventory remains outstanding. The November 14, 2026 manuscript target is conditional. No causal effect is established.

Next: independently authenticate SEC inputs and the fixed treatment roster, freeze exchange-session coverage, then run historical September trends and October placebos with HAC-lag sensitivity and pair/block-bootstrap checks.
