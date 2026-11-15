# Phase 377 — Exact matched-pair leave-one-out influence audit

**Status:** Methodological validation only; November 14, 2026 publication deadline missed and manuscript uncertified.

Extends Phase 376's equal-pair-weight matched-date contrast. For N matched pairs with pair effects d_i and overall mean D, removing pair i yields (N D - d_i)/(N - 1). The implementation computes all N deletion contrasts exactly using rational arithmetic and independently recomputes each from filtered source rows. It reports the minimum, maximum and whether any nonzero deletion contrast has the opposite sign to the nonzero full estimate. A zero full or deletion estimate is not classified as a sign reversal. At least two pairs and Phase 376's fully balanced pair-date-arm grid are required.

**Constructed-data verification:** Seven deterministic local unittest cases passed (exact deletion, sign reversal, no reversal, single-pair rejection, incomplete grid rejection, integer precision above 2^53, and zero-estimate behavior). The local Phase 376 dependency was reconstructed from the GitHub connector's retrieved file; the exact published checkout and full suite remain untested. Run `PYTHONPATH=scripts python -m unittest discover -s tests -p 'test_phase377_pair_influence.py'`.

**Interpretation:** Leave-one-pair-out sensitivity is a diagnostic, not a standard error, p-value or solution to shared-date dependence. It cannot establish parallel trends or causal identification. The September pretrend warning, substantial October placebo behavior, original 78 dated placebo estimates, historical treatment authentication, source-data provenance, selection/weighting effects, exchange controls and matched-group plus common-date/serial-dependence-aware inference remain unresolved. No authenticated SEC observations or historical ZIPs were used/imported; no empirical result or causal effect is asserted.

**Next gate:** Authenticate source observations and treatment assignments; reconstruct dated placebo estimates and pretrends; then apply this influence diagnostic alongside pair-cluster and date-aware uncertainty rather than treating deletion ranges as confidence intervals.
