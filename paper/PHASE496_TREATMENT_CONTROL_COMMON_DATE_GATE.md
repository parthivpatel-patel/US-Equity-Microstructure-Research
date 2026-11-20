# Phase 496 — Treatment/control common-date admission gate (2026-11-20)

## New verified result

A locally executed independent Python prototype passed **8/8 deterministic pytest tests** (0.07 seconds). The prototype rejects duplicate keys, malformed cutoffs, out-of-universe observations, missing treatment/control groups, incomplete observations and insufficient common dates. It admits a fully observed two-security constructed fixture with one shared pre-date and one shared post-date. These are **constructed fixtures, not SEC observations**.

The prior Phase 495 intersection over *fully covered* units can conceal excluded partially covered units: a nonempty intersection among the survivors does not establish full eligible-unit support. The new gate instead requires **every two-sided eligible security-exchange unit** in an exchange to be fully covered, requires both treated and control units, and intersects observed dates across all those units. It then requires at least one shared pre-date and post-date (configurable threshold). This is a deliberately conservative sample-admission rule, **not** a causal estimator or a recommendation to silently drop exchanges.

### Reproduction and disclosure

The locally executed prototype and eight tests are retained at `/mnt/data/phase496/` in the session execution environment, but **are not part of this GitHub commit**. Do not represent the repository as having executable Phase 496 tests until they are separately published and executed from a clean checkout. No historical data or estimates were used.

This gate does not establish treatment authenticity, SEC data provenance, stable matching, weighting invariance, parallel trends, September pretrends, the substantial October placebo warning, serial dependence, or causal identification. Even passing the conservative support gate does not establish any of those conditions.

### Outstanding artifact inventory

- Phase 430 and 436 historical archives: not authenticated or imported.
- Phase 472 executable package: not authenticated or imported.
- Phase 496 local prototype and tests: locally tested, not yet synced.
- Historical SEC source records and date-specific treatment/eligibility: not authenticated in this session.

The November 14, 2026 deadline was missed. The manuscript remains **not publication-certified**. Next action: publish the exact tested prototype and tests, rerun from GitHub, authenticate historical observations and date-specific round-lot assignments, then apply the gate by exchange before placebo/pretrend inference.
