# Phase 192 — Outcome pairing and fixed-roster eligibility (2026-11-06)

## Executed verification
A new standard-library Python audit and seven deterministic unittest cases were executed locally; all seven passed. These are constructed observations and **not** historical SEC estimates.

## Identification and sample construction
A balanced count and volume sample requires matching **security ID, exchange, matched-group ID, and trade date**, not just equal numbers of observations. Equal sample counts can conceal entirely different security/group identities. The new audit checks duplicate composite keys, finite contrasts, date format, exact count/volume pairing within every security/exchange/group/date unit, and fixed roster membership across dates. It returns a fail-closed eligibility flag for a fully paired fixed-roster common-date descriptive analysis.

The strict full-roster rule is a diagnostic, not an assertion that a balanced panel is the only valid research design. Attrition and outcome-specific missingness must be reported, and any restricted common sample must be compared with the original estimand. A weekday is not proof of an exchange trading session. This script does not independently authenticate SEC source bytes, Nasdaq historical treatment, matching validity, licensing, or identifier continuity.

## Historical evidence status
No authenticated original daily observations or historical ZIP archives were recovered in this session. Therefore this checkpoint provides no new historical coefficients, pretrend estimates, placebo p-values, or causal claims. The substantial October 2025 placebo warning, September pretrends, treatment authentication, selection/weighting sensitivity, security/exchange controls, and serial-dependence-aware inference remain unresolved.

## Reproduction
Run `python -m unittest -v tests/test_phase192_pairing_gate.py` from a checkout with `scripts` on PYTHONPATH, or `cd scripts && python -m unittest discover -s ../tests -p test_phase192_pairing_gate.py`. Execute the audit as `python scripts/phase192_pairing_gate.py input.csv` with the Phase 191 CSV schema. The seven tests were executed locally before publication; fresh-checkout execution of the exact published files remains pending.

## Next action
Recover original authenticated daily observations and provenance manifests; apply Phase 191 checksum/provenance checks followed by this exact outcome/roster audit, then evaluate fixed-roster common-date placebos and two-way clustered inference. November 14, 2026 remains a conditional publication target. No causal effect established.
