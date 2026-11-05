# Phase 168 — Calendar-date integrity in matched daily contrasts

Date: 2026-11-05. Scope: methodological validation only; no historical SEC data used.

## Finding
The Phase 167 `paired_dates` routine validates date identifiers only as nonempty strings and partitions them using lexical `d < cutoff` comparison. Its ordering is reliable only if every date and cutoff has the same canonical sortable representation. An input such as `2025-9-30` can therefore be incorrectly ordered against `2025-10-01`. Invalid calendar dates are also accepted by that earlier routine.

The new Phase 168 implementation requires canonical ISO `YYYY-MM-DD` dates, verifies actual calendar validity, and compares parsed `datetime.date` objects. It preserves duplicate-cell rejection, complete matched-arm checks, available-case contrasts, and fixed balanced-roster contrasts. It deliberately does not silently impute incomplete pairs.

## Verification and provenance
A local independently written prototype passed ten unittest cases on 2026-11-05, including canonical date admission, impossible dates, non-padded dates, timestamps, duplicate cells, incomplete pairs, invalid arm/outcome, changing group composition, and absence of a balanced roster. The published companion implementation has its own ten tests. The published file was not executed in a fresh checkout during this session; do not conflate local prototype validation with CI confirmation.

Constructed composition example: available-case date contrasts [0,0,5,5], balanced-roster contrasts [0,0,0,0]. These are demonstration values, not SEC estimates. A balanced roster is a sensitivity specification, not a guaranteed unbiased estimand.

## Identification and release gates
The substantial October 2025 placebo warning and September pretrends remain unresolved. Treatment labels require authentication against original Nasdaq historical round-lot rules and source snapshots; the 68 provisionally treated names are not yet independently certified. Exchange/security fixed effects, matched-group dependence, common-date shocks, serial dependence, selection and weighting sensitivity must be evaluated on authenticated source observations before any causal claim.

## Historical archive inventory status
Previously reported private artifacts: `roundlot_phase2.py`, `roundlot_phase2_security_panel.csv`, `roundlot_pilot_daily.csv`. Their presence and redistribution permissions were not reverified this session. Historical research ZIPs, SEC daily source archives, and Nasdaq snapshots remain unimported and unverified for this session. No proprietary data, source archives, or synthetic figures were uploaded.

## Next
Recover and hash original SEC/Nasdaq files, verify symbol-to-lot treatment mapping, audit date/exchange/security keys, and run September/October placebo scans with fixed common-date support and matched-group/serial-dependence-aware inference. Publication target November 14, 2026 is conditional; no causal effect established.
