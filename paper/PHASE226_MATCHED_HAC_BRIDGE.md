# Phase 226: matched panel to joint-window HAC bridge

Date: 2026-11-07. Independent U.S. equity microstructure study.

## Method
The new bridge calls the published Phase 225 strict matched security/exchange/date panel gate and then the published Phase 224 full-series Bartlett HAC estimator. Unlike the Phase 225 separate-window bootstrap, the HAC score series includes cross-window covariance. Every matched pair and exchange receives equal weight. The duplicated input to Phase 224's two contrast slots is a compatibility mechanism; the bridge returns only the equal-cell result, and does **not** claim to compute pooled-execution weighting.

## Verification status
Both dependency source files were read via the connected GitHub tool before implementation. Local Python syntax compilation succeeded. Running the seven integration tests failed at import time because Phase 225 was not available locally; downloading the dependency from raw.githubusercontent.com failed due to DNS resolution. **No test-pass claim is made.** The new code and tests are provisionally published for exact-checkout verification.

## Historical inference limitations
This bridge does not authenticate SEC observations, Nasdaq treatment assignments, exchange sessions, or historical matched rosters. It does not supply security-cluster inference. The September pretrends and substantial October 2025 placebo warning remain unresolved; no reform causal effect is established. Full-panel admission may create complete-case selection bias. No historical data or research archives were imported.

## Next verification
In a clean checkout run `PYTHONPATH=scripts python -m unittest discover -s tests -p 'test_phase226_matched_hac_bridge.py' -v`. Authenticate source panel, exchange sessions, and historical treatment roster before historical estimation; compare equal-cell with pooled-execution estimands and security-cluster sensitivity.
