# Phase 242 — Fixed-width common-date placebo cut scan

Date: 2026-11-08. Independent U.S. equity round-lot research.

## Implementation and verification
Inspected the published Phase 224 HAC estimator and Phase 238 bandwidth wrapper before creating this additive scan. The new `placebo_scan` uses a common fixed number of dates on either side of every candidate cut and calls Phase 224 separately for equal-cell and pooled-count contrast series. It rejects duplicate cuts, insufficient windows, invalid bandwidths, unordered dates, and nonfinite observations (via Phase 224).

Six deterministic unit tests passed locally using a transcription of the GitHub-published Phase 224 implementation, **not a verified repository checkout**. A synthetic linear fixture yielded differences 2 and 4 for equal-cell and pooled-count series respectively at each of three candidate cuts. The fixture uses fabricated date labels, including weekends; it is solely a numerical software test, not an authenticated trading calendar or empirical market analysis.

## Interpretation boundaries
The scan does not authenticate SEC inputs, exchange calendars, treatment assignment, fixed security rosters, or matched controls. Adjacent placebo windows overlap, so treating cut-specific statistics as independent tests is invalid. No multiple-testing adjustment or security-cluster inference is provided. Candidate cut dates and bandwidths should be prespecified, and an authoritative trading calendar should be verified before historical application. In particular, the substantial October 2025 placebo and September pretrends remain unresolved; a positive placebo cannot be dismissed as noise.

## Next steps
Run the exact committed test against a verified checkout/CI, authenticate SEC raw files and treatment rosters, then construct a complete common-date fixed-roster panel with exchange/security controls. Compare September and October placebo cuts with the November reform, report weighting and bandwidth sensitivity, and add serial- and security-dependence-aware inference. No causal effect has been established. Recovered archives remain unavailable for verified inventory/import.
