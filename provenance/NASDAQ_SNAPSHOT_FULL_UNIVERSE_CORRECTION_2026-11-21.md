# Corrected full-universe Nasdaq snapshot reconciliation (2026-11-21)

**Evidence:** direct reparse of the two third-party snapshot CSVs and exact symbol comparison with the recovered 2,262-row processed security panel. Not official Nasdaq effective-date certification or SEC source authentication.

## Material correction to earlier published counts

The earlier snapshot audit reported **86** non-100 entries per snapshot. That calculation included **two non-security trailer/empty records** in each source: the `File Creation Time: ...` trailer and a blank row, both with empty Round Lot Size fields. Re-reading each CSV using quote-aware CSV parsing, filtering to actual security rows, and accepting numeric round-lot fields yields **84 securities** in each snapshot: **80 with 40 shares and 4 with 10 shares**. Total valid security records: **5,159** (November 1 commit) and **5,222** (December 1 commit); prior 5,161/5,224 totals included the two non-security records. There are 5,075 and 5,138 valid 100-share securities, respectively.

Thus the earlier **68/86 = 79.07%** figure and **18 unmatched entries** were incorrect as a security-level denominator. Corrected: **68/84 = 80.95%**, leaving **16 non-100 securities outside the provisional 68-name cohort**. The two third-party snapshots contain the same 84 non-100 tickers and their round-lot fields agree across dates.

## Exact full-universe membership reconciliation

The 68 previously reported provisional treated tickers all match non-100 fields (64 at 40 shares, 4 at 10 shares). The **16 remaining non-100 tickers** are: `ARGX, ASML, BRKRP, CYBR, EQIX, ESLT, LIN, NVMI, ONC, QQQ, RTH, SMH, SOXX, VONE, VTHR, WTW`. Exact case-sensitive ticker comparison against **all 2,262** `Ticker` entries in the recovered `roundlot_phase2_security_panel.csv` finds **zero** of these 16 in the processed panel. Therefore the 16 do **not** appear as exact-symbol provisional controls in that file. This resolves the narrow exact-symbol control-leakage question for these snapshots, **not** alias/corporate-action mapping or actual November 3 treatment.

| Classification | 2025-11-01 | 2025-12-01 |
|---|---:|---:|
| Valid snapshot security records | 5,159 | 5,222 |
| 100-share field | 5,075 | 5,138 |
| Non-100 field | 84 | 84 |
| Non-100 exact matched to provisional treated | 68 | 68 |
| Non-100 exact matched to provisional controls | 0 | 0 |
| Non-100 absent from processed panel | 16 | 16 |
| Excluded non-security trailer/blank records | 2 | 2 |

## Source and processing limits

- [Snapshot 1, commit 441144e](https://raw.githubusercontent.com/datasets/nasdaq-listings/441144e/data/nasdaq-listed-symbols.csv); [snapshot 2, commit 2ca384c](https://raw.githubusercontent.com/datasets/nasdaq-listings/2ca384c/data/nasdaq-listed-symbols.csv). Third-party GitHub history is **not** original Nasdaq source verification.
- Processed panel: `roundlot_phase2_security_panel.csv`, previously recorded SHA-256 `2ccb80427a765ca3858f11f2874d6f87a79a559ec1fdeafc34420e82840e5bbb`. Its hash identifies processed bytes, not SEC original records.
- Method: parse CSV quoting; identify the `Symbol` and `Round Lot Size` columns; exclude file-creation trailer and blank row; group only actual security symbols with numeric size fields; exact-match against the full panel ticker set. The snapshot dates reflect Git commits, not necessarily effective-date records.
- This correction supersedes the 86/18 arithmetic in `provenance/NASDAQ_GITHUB_SNAPSHOT_CROSSCHECK_2026-11-21.md` and `paper/TREATMENT_COVERAGE_SELECTION_WARNING_2026-11-21.md`; those prior reports are retained for audit history. Do not cite their uncorrected security counts.

**Interpretation:** No exact-symbol provisional-control overlap was observed among the 16 additional snapshot non-100 securities. No causal identification is established. Official September price evaluation, effective-date symbol directory, SEC original ZIP authentication, daily falsification and clustered/bootstrap inference remain required.
