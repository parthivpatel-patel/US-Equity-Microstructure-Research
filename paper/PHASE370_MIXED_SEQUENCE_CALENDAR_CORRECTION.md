# Phase 370 — mixed-sequence calendar validation correction

## Scope and reproducibility
The Phase 369 validator explicitly permits both lists and tuples for trading sessions and event dates. Its original validation expression `sessions + event_dates` raised an unexpected `TypeError` whenever one input was a tuple and the other was a list. The corrected expression `(*sessions, *event_dates)` validates the same elements without relying on matching sequence types.

Five focused deterministic prototype tests passed locally on November 14, 2026: tuple/list, list/tuple, tuple/tuple, datetime rejection, and the nine-shared-session overlap invariant for adjacent ten-session constructed windows. Run the published regression with `python -m unittest discover -s tests -p 'test_phase370_mixed_sequences.py'` from the repository root. The exact published checkout and complete repository suite have not yet been executed.

## Research limitations and certification
These fixtures are constructed dates, not authenticated trading sessions or SEC market observations. No reform effect was estimated. Historical September pretrends, the substantial October placebo warning, treatment-assignment authentication, original 78 dated placebo estimates, Phase 130 contradiction, source-byte provenance, and dependence-aware inference remain unresolved. No historical ZIP archives were recovered in this session. The November 14, 2026 publication target has not been met; manuscript certification is withheld.

## Next empirical task
Recover the actual dated placebo estimates and original source-byte manifest, validate the historical exchange trading calendar, then rerun placebo comparisons with security/exchange controls and matched-group plus common-date and serial-dependence-aware uncertainty. Do not interpret exploratory placebo ranks as calibrated p-values.
