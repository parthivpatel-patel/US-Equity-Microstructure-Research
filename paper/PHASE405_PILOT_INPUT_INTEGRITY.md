# Phase 405 — Recovered pilot input-integrity audit (2026-11-16)

## Directly executed source-data check

Recovered the Library's original `roundlot_pilot_daily.csv` (12,054 bytes) and ran `scripts/phase405_date_coverage.py` against the raw file. Local SHA-256: `9cd1e7f9fc89a2254211868e1a82cf97fd243bc860ad03eefa99409f94086bba`. The script accepts the file's actual numeric tier representation (`10.0`, `40.0`, `100.0`), rather than rejecting these as malformed integers.

Observed results: **126 rows**, **42 distinct dates**, from **2025-10-01** to **2025-11-28**; **23 October dates** and **19 November dates**. Every date has all three 10/40/100 tiers; zero duplicate date-tier rows, zero weekend dates, and zero invalid or missing tested numerator/denominator pairs. The structural completeness check passed. Seven deterministic unit tests passed locally.

This check is limited to **internal structure and arithmetic bounds**, not SEC authenticity, original data licensing, source coverage, historical lot classification, or numerator definitions. It does not establish that the observed date list exhausts the official exchange calendar. In particular, the file has **no September records** and cannot support September pretrend estimation, security/exchange controls, or matched-control inference. It also does not resolve the material October placebo warning.

## Reproduction

```sh
PYTHONPATH=scripts python -m unittest discover -s tests -p 'test_phase405_date_coverage.py'
python scripts/phase405_date_coverage.py /path/to/roundlot_pilot_daily.csv
```

The original CSV was **not** uploaded because its redistribution rights and upstream provenance are unverified. The SHA-256 above allows comparison with a separately authorized copy.

## Next gate

Recover authenticated SEC security-exchange-day files, contemporaneous lot assignments, September observations, the 204 matched-control mapping and original dated placebo outputs. Perform security/exchange controls and date/serial-dependence-aware inference only after those inputs are validated. November 14 deadline missed; November 30 remains provisional; no causal claim or publication certification.
