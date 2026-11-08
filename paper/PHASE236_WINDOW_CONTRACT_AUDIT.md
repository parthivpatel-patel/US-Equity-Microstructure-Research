# Phase 236: Strict window contract and remaining authentication boundary

2026-11-08. Independent U.S. equity round-lot reform study. No historical SEC data analyzed in this phase.

## Verified source audit
Phase 235 validates date ordering and requested roster membership but does not enforce canonical ISO dates for requested sessions and does not explicitly require both early and late windows to be nonempty. It calls the Phase 234 structural calendar validator, which cannot establish holiday or ad hoc exchange closure authenticity. The new additive window guard rejects empty windows, noncanonical dates, duplicate or unsorted dates, mismatched partitions, and requested dates missing from the supplied calendar. It never claims independent calendar authentication.

## Reproduction
Run `python -m unittest -v test_phase236_window_guard.py` from a directory containing the script and test, or set PYTHONPATH to scripts and run the test from tests. Local Python unittest: 11 tests passed (2026-11-08). The tests use deterministic synthetic date fixtures. They do not exercise the complete Phase 226 estimator or the Phase 235 integration, and do not establish historical data validity.

## Next action
Integrate this guard into the live estimator preflight without weakening existing checks; authenticate SEC source bytes, exchange calendar and treatment mapping; rerun fixed-roster October placebo, September pretrends, exchange controls, weighting sensitivity and dependence-aware inference. No causal claim is warranted. Previously recovered archives not accessible in this run; complete publication inventory remains unverified.
