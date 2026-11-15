# Phase 371 — structural panel integrity gate (November 14, 2026)

## Scope
A standard-library, fail-closed CSV audit was implemented and tested locally. It checks unique security-date-exchange keys, stable security-level treatment/control labels, canonical ISO dates, nonempty identifiers, finite nonnegative integer-valued count/share measures, and hidden numerators not exceeding corresponding totals. It reports panel dimensions without disclosing underlying licensed data.

## Verification
Eight deterministic unittest cases passed locally on constructed fixtures (valid two-security panel, duplicate key, cohort switch, NaN measure, impossible numerator/denominator, malformed date, empty panel, fractional count). No original SEC observation was loaded; no empirical effect was estimated. Run: `python -m unittest discover -s tests -p 'test_phase371_panel_gate.py'`.

## Important scope limitation
This schema is an explicit *input contract*, not a claim that the SEC download uses these exact column names. A documented transform from authenticated source columns to this canonical panel is still required. Neither a structural pass nor a SHA-256 match authenticates the original publisher, treatment assignment, exchange eligibility, data rights, or causal identification. The script does not claim otherwise.

## Outstanding empirical barriers
Original 78 dated placebo estimates and SEC source bytes remain unavailable for authenticated reanalysis. September pretrends, substantial October placebo, Phase 130 contradiction, selection/weighting sensitivity, and matched-group/common-date/serial-dependence-aware inference remain unresolved. Recovered historical ZIP inventory and imports are still pending. November 14 publication target was not met; manuscript is uncertified.

## Next
Recover source manifests and dated placebo files; verify provenance and permitted redistribution; map original source columns to the canonical panel; run the gate on actual observations; only then execute pretrend/placebo/inference estimators. No causal effect is asserted.
