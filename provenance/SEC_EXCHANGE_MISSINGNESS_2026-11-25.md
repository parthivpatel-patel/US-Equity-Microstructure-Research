# Exchange missingness audit — 2026-11-25

Actual user-uploaded Q3/Q4 2025 SEC-format archives, six monthly CSVs; independent source-byte authentication remains pending. Filter Security == Stock. Count missing numerator or denominator separately for Hidden/TradesForHidden and HiddenVol('000)/TradeVolForHidden('000). Count zero denominators separately. Results for both metrics coincide in aggregate (not a claim of rowwise equivalence).

| Exchange | Rows | Missing pairs per metric | Zero denominators per metric |
|---|---:|---:|---:|
| Amex | 433657 | 0 | 48141 |
| Arca | 471739 | 0 | 5204 |
| Bats-Y | 467786 | 0 | 24699 |
| Bats-Z | 471745 | 0 | 12049 |
| Boston | 456794 | 0 | 38986 |
| CHX | 369011 | 0 | 112096 |
| Edge-A | 471071 | 0 | 56151 |
| Edge-X | 471728 | 0 | 5368 |
| IEX | 465055 | 465055 | 0 |
| MEMX | 470618 | 0 | 19081 |
| MIAX | 466974 | 0 | 44040 |
| NSX | 420973 | 0 | 29095 |
| NYSE | 470815 | 0 | 36042 |
| Nasdaq | 471734 | 0 | 2616 |
| Phlx | 460093 | 0 | 83323 |
| Total | 6839793 | 465055 | 516891 |

All missing pairs are concentrated in IEX. Do not impute zero rates for missing or zero denominators. This is a descriptive coverage audit, not treatment identification or a causal estimate. Historical 14-exchange panel reconciliation remains pending.

Reproduction: pandas read_csv on each CSV inside each ZIP, chunksize=200000; filter Stock; group by Exchange; sum row counts, (numerator.isna() | denominator.isna()), and (denominator == 0) separately for each metric. No raw data redistributed.
