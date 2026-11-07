# Phase 209: Pre-reform placebo-window admission

Date: 2026-11-07. Independent round-lot research; no GIG project dependencies.

## Purpose
A November 3, 2025 reform effect cannot be inferred from a post-minus-pre comparison if a substantial October 2025 placebo contrast and September pretrends already exist. This checkpoint introduces a strict date-window admission gate before historical placebo estimation.

The implementation rejects empty, duplicate, unordered, noncanonical, overlapping, interleaved, undersized, out-of-panel and post-reform placebo windows. It deliberately does not generate a trading calendar or authenticate the supplied observations. It returns explicit false flags for source authentication, treatment authentication and causal establishment.

## Verification
An independently executed local prototype passed 11 deterministic synthetic tests on 2026-11-07 (unittest). The published script and test module have equivalent admission logic, but their exact committed versions have not yet been executed from a clean checkout. Constructed dates are weekdays, not an independently authenticated exchange calendar. No historical SEC coefficient or statistical inference was computed.

## Identification and inference limitations
The gate does not address the existing September pretrend, the large October placebo, security/exchange composition, matched-control validity, weight sensitivity, serial dependence, or multiple placebo-date selection. These remain mandatory gates before any causal interpretation. Source records, Nasdaq round-lot assignments, original recovered ZIPs and historical analysis outputs were not imported this session.

## Next
Run the published tests from a clean checkout; recover authenticated SEC observations and the historical treatment mapping; enumerate pre-specified September and October placebo dates using a verified trading calendar; apply Phase 207–208 fixed-roster matched-group contrasts and HAC sensitivity; compare equal-security, equal-group and volume weights. Do not call the paper complete before independent reproduction and source authentication.
