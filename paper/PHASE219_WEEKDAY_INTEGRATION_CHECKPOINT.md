# Phase 219: weekday fixture integration regression

Date: 2026-11-07. Scope: independent round-lot reform methodology only.

The previously published Phase 216 integration test fixture includes weekends. Phase 218 provides a weekday-only synthetic fixture, but its integration with Phase 216 was not covered by a published regression test. This checkpoint adds four tests connecting the Phase 218 fixture to the Phase 216 admission-plus-HAC interface: weekend exclusion, expected 10/10 windows and four intervening sessions, missing-session rejection, reform-date boundary, and availability of the prespecified lag outputs.

Verification: Four tests passed locally on 2026-11-07 against **locally reconstructed stand-ins** of the repository's Phase 213, 215, 216, and 218 modules, not the exact GitHub versions. Therefore this is **not** a verified clean-checkout test pass and should not be represented as such. The new test file must be executed against the exact published repository modules before marking this integration validated.

The weekday-only fixture does not exclude market holidays; it is not an authenticated exchange calendar. No SEC observations, treatment assignments, historical estimates, placebo results, or research archives were authenticated or imported here. The substantial October 2025 placebo warning, September pretrends, composition/weighting sensitivity, and identification remain unresolved. No causal claim is supported.

Next: run this regression on a clean repository checkout, authenticate official trading sessions and SEC source data, then compute fixed-roster common-date matched-group pretrends and October placebo diagnostics with dependence-aware inference. Keep the November 14 manuscript target conditional.
