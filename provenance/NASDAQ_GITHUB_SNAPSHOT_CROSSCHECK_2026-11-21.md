# Historical Nasdaq listing snapshots: independent roster cross-check (2026-11-21)

## Sources inspected
- [Automated listing snapshot committed 2025-11-01 01:01:35 UTC](https://github.com/datasets/nasdaq-listings/tree/441144e), raw [CSV](https://raw.githubusercontent.com/datasets/nasdaq-listings/441144e/data/nasdaq-listed-symbols.csv).
- [Automated listing snapshot committed 2025-12-01 01:11:41 UTC](https://github.com/datasets/nasdaq-listings/tree/2ca384c), raw [CSV](https://raw.githubusercontent.com/datasets/nasdaq-listings/2ca384c/data/nasdaq-listed-symbols.csv).

These are **third-party GitHub snapshots**, not authenticated contemporaneous Nasdaq official files. Commit timestamps are GitHub metadata, not proof of the source's measurement timestamp, exchange authenticity, or November 3 effective treatment.

## Direct CSV comparison
The two UTF-8 CSVs were retrieved via the connected GitHub resource interface and parsed using a quote-aware CSV field splitter. The October-end snapshot has **5,161** data records and **86** records whose `Round Lot Size` field is not the literal `100`. The November-end snapshot has **5,224** data records and **86** such records. **Zero** symbols present in both snapshots have a changed `Round Lot Size` field. This does **not** mean zero symbols experienced reform treatment: additions/deletions, stale or erroneous third-party fields, and the distinction between existing round-lot records and effective-date assignments preclude that inference.

This cross-check provides a reproducible *lead* for roster verification, not an authenticated treatment roster. In particular, **86 non-100 records cannot be equated to the 68 provisional treated symbols** in the separate processed study panel without symbol-level joins and historical reference-price/effective-date validation. No causal analysis, SEC source authentication, or new treatment certification is claimed.

## Reproduction
Download both linked CSV files; parse RFC-style quoted commas; key by `Symbol`; compare `Round Lot Size` only on the intersection. Count non-`100` values in each entire snapshot separately. Verify both GitHub commit dates through the commits API. Do not distribute these files as original Nasdaq source material.

## Remaining verification
Obtain the contemporaneous official September 2025 evaluation, official effective November 3 symbol mapping and symbol/corporate-action continuity; then compare against the 68 provisional panel names. Original SEC Q3/Q4 ZIP authentication remains separately blocked (HTTP 403 on the hosted runner).