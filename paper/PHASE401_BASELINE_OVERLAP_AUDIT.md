# Phase 401 — Historical Phase 2 baseline imbalance and empirical overlap audit

**Date:** 2026-11-16. **Status:** descriptive sensitivity audit, not causal identification.

Input: previously recovered Library file `roundlot_phase2_security_panel.csv` (2,262 rows; 68 provisionally treated, 2,194 controls). The original raw SEC Q4 archive and historical November 3 round-lot assignments have **not** been authenticated; the source CSV is not redistributed.

Using treated/control means and standardized mean differences (SMD; pooled within-group sample variance), baseline hidden trade-count rates were 0.490516 versus 0.344845 (SMD **1.9026**); baseline hidden share-volume rates were 0.492960 versus 0.291590 (SMD **2.4943**); log(1 + preperiod trade count) was 12.818053 versus 10.822600 (SMD **1.3391**). These are unusually large observed baseline imbalances.

Pooled-sample baseline quartiles show weak common support. For hidden trade-count baseline quartiles, treated counts were **0, 0, 4, 64** versus control counts **566, 565, 561, 502**. For hidden share-volume baseline quartiles, treated counts were **0, 0, 2, 66** versus controls **566, 565, 563, 500**. Treated-minus-control mean changes within occupied trade-rate quartiles were **+0.036359** (quartile 3 of 4, 4 treated) and **−0.020662** (quartile 4, 64 treated). Corresponding share-volume change contrasts were **−0.017420** (2 treated) and **−0.004033** (66 treated). These are exploratory subgroup comparisons, not reliable treatment effects or confidence intervals; the 2- and 4-treated strata are especially unstable.

**Interpretation:** Broad controls are strongly compositionally different even before reform. Naive full-sample contrasts, regression adjustment and global matching are highly sensitive to common-support assumptions. Quartile occupancy is not a complete multivariate propensity-score overlap analysis. No matched 204-control roster or security-by-date-by-exchange observations were available for this run.

**Verification:** five deterministic tests passed locally against a closely related implementation, and the recovered historical CSV was read and analyzed directly. Published file bytes were checked through GitHub after commit, but the exact published checkout and full repository suite were not executed. Run with `PYTHONPATH=scripts python -m unittest discover -s tests -p 'test_phase401_overlap.py'` and `python scripts/phase401_overlap.py local_panel.csv`.

**Release gate:** The October 2025 placebo, September pretrends, original 78 dated placebo estimates, treatment authentication, exchange effects, matched controls and serial/common-date dependence-aware inference remain unresolved. The November 14 deadline was missed; November 30 is provisional. No causal claims or publication certification.

**Next:** authenticate original SEC Q3/Q4 source archives and historical lot assignments; recover daily security-exchange panel and matched roster, then implement overlap-restricted comparisons and common-date/block inference.
