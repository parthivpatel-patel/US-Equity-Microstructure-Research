# Phase 278 — Leave-one-exchange-out sensitivity

The fixed-roster Phase 277 audit returns daily pair-weighted and exchange-equal contrasts. Phase 278 adds an exchange-influence diagnostic: omit each exchange, recompute the *time mean* of the daily contrasts under both weighting conventions, and flag strict sign reversals relative to the full sample.

This is a descriptive influence check, not a standard error, causal estimate, exchange fixed-effects model, or substitute for matched-group/common-date inference. A zero full-sample or omitted-sample contrast is not called a sign reversal. An exchange with more pairs contributes more to the pair-weighted estimator; every exchange receives the same weight in the exchange-equal estimator.

Synthetic illustration only: with two pairs on exchange X having contrast -2 and one pair on Y having contrast +5, the pair-weighted mean is 1/3 and the exchange-equal mean is 1.5. Omitting Y yields -2 under both conventions, a strict sign reversal. These are **constructed inputs**, not SEC data or historical findings.

Usage: first call `scripts/phase277_exchange_balance.py:audit_panel` on a fixed complete pair/date/exchange panel; pass its returned dictionary to `leave_exchange_out`. The Phase 278 module has no external dependencies. To run tests from repository root: `PYTHONPATH=scripts python -m unittest discover -s tests -p 'test_phase278_leave_exchange_out.py'`.

Local validation on a standalone equivalent source: 10 deterministic unittest cases passed on 2026-11-09. The exact published GitHub checkout and full test suite were not rerun. The source calendar, roster, SEC input observations, treatment mapping, and exchange assignments remain unauthenticated; output flags explicitly deny historical authorization.

**Outstanding:** authenticate original SEC downloads and checksums; verify session calendar and November 3 round-lot assignments; freeze matching before analysis; reproduce September pretrends and substantial October 2025 placebo findings; compare security/exchange controls, alternative outcome definitions, HAC lags and date/security cluster bootstraps. Recovered historical ZIPs, earlier manuscripts and charts remain unimported and require inventory and redistribution review. No causal conclusion is warranted.
