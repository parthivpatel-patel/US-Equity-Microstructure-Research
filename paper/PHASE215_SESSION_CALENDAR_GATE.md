# Phase 215: Explicit session-calendar completeness gate

Date: 2026-11-07. Scope: constructed-input software validation only.

Phase 213 computes joint-window HAC scores in observation order. An omitted trading session can therefore silently alter lag distances, and an extra or duplicate date can alter sample composition. Phase 215 introduces an explicit supplied-session gate: observed contrast dates must exactly equal a unique, ordered, strictly pre-reform session calendar; window endpoints must be actual sessions; windows cannot overlap. The output counts intervening **sessions**, not calendar days.

Eleven deterministic unit tests passed locally on a constructed six-session October example. The example includes a weekend and yields two intervening sessions. This is not an authenticated historical exchange calendar or SEC observation. No historical coefficients, empirical figures or causal findings were produced.

The gate intentionally returns calendar_authenticated=false, source_authenticated=false and treatment_authenticated=false. It cannot verify whether a supplied calendar is authentic, whether the matched roster is complete, or whether treatment assignments reflect original Nasdaq round-lot classifications. It must precede Phase 213, not replace fixed-roster, common-date matching, security/exchange controls, weighting sensitivity, September pretrend tests or October placebo analysis. HAC inference still requires bandwidth and cross-sectional-dependence sensitivity.

Archive inventory: no recovered historical ZIPs or paper/chart packages were available for authenticated import during this session. No archive files were published. Next: clean-checkout test execution, source and calendar provenance authentication, then historical September and October estimates. The November 14 target remains conditional; no causal reform effect is established.
