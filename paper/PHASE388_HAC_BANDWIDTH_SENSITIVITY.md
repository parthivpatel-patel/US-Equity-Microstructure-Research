# Phase 388: HAC bandwidth sensitivity gate

This phase extends Phase 387 without changing its published implementation. It computes Bartlett HAC long-run variance and variance of the mean at multiple bandwidths on the same balanced matched-pair/date panel. It retains exact rational arithmetic, canonical dates, duplicate rejection, and equal pair weighting. Date shocks remain aligned across pairs.

## Constructed validation
For two identical matched-pair sequences over four dates, [0,1,0,1], the mean is 1/2. Bartlett bandwidth 0 gives variance of the mean 1/16; bandwidth 1 gives 1/64. The difference illustrates bandwidth sensitivity **only**. A constant sequence returns zero variance with an explicit warning; zero must not be interpreted as certainty.

Ten deterministic local regression tests passed on 2026-11-15. Run from repository root with `python -m unittest tests/test_phase388_hac_bandwidth_audit.py` (or use unittest discovery if the tests directory is not a package). The published checkout and complete repository suite have not been run.

## Interpretation limits
No authenticated SEC observations were analyzed in this phase. HAC on the cross-pair date means does not jointly address pair-level sampling dependence, exchange selection, treatment authentication, nonstationarity, or the identification problem. A variance estimate is not a confidence interval or causal finding. Serial dependence is indexed by *observed sessions*, not elapsed calendar days. The balanced-panel requirement can induce selection bias. Do not use this tool to erase September pretrends or the substantial October placebo warning.

## Publication gate and outstanding inputs
November 14, 2026 target missed; paper uncertified. Authenticate original source files and historical treatment roster, recover 78 original dated placebo estimates, inventory recovered historical archives and permissions, quantify balanced-panel attrition, and run matched-pair/date and serial-dependence-aware sensitivity on the actual panel before publication.
