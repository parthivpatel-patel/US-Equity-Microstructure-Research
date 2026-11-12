# Phase 317 — Historical placebo tail semantics (2026-11-12)

## Source and method
Read the existing public `results/phase130_summary.csv` through the connected GitHub file API. Developed a read-only, standard-library audit and seven synthetic-fixture tests. Seven tests passed locally against the corresponding logic. This is a frozen-summary integrity audit, **not** new estimation from authenticated SEC observations or an independent replication of the underlying 78 placebo windows.

## Descriptive results
| Outcome | Event contrast (pp) | Windows | Reported at-least-as-negative | Reported at-least-as-extreme absolute | Absolute minus negative |
| --- | ---: | ---: | ---: | ---: | ---: |
| Hidden execution count | −0.7346606598677254 | 78 | 2 | 2 | 0 |
| Hidden execution volume | +0.626597999820323 | 78 | 48 | 76 | 28 |

The **at-least-as-negative** count is a *lower-tail* count. For the **positive volume** contrast, 48/78 is not a right-tail count and cannot be interpreted as directional evidence for a positive effect. The 76/78 absolute-extreme count is two-sided in magnitude only; it is not a calibrated two-sided p-value. For a negative count contrast, every placebo value at least as negative is also at least as extreme in absolute magnitude, so the observed 2 <= 2 is logically consistent. For a positive volume contrast, no such nesting holds; the difference of 28 is merely a difference between two reported counts and does **not** recover a right-tail frequency or underlying sign distribution.

The placebo windows overlap, may contain other events, and were evaluated post hoc. The October 2025 announcement is an information event, not a clean placebo; September pretrends remain concerning. No source-byte authentication, historical treatment verification, common-date dependence-aware inference, exchange/security control estimation, or archive import was completed in this phase.

## Reproduction
```bash
python -m unittest discover -s tests -p 'test_phase317_placebo_semantics.py'
python -m scripts.phase317_placebo_semantics results/phase130_summary.csv
```

The audit rejects malformed CSV headers, duplicate/missing outcomes, non-finite values, impossible counts, event contrasts outside the reported historical range, and inconsistent negative-tail/absolute counts. Tests use synthetic fixtures; no synthetic output is passed off as research data.

## Publication gate
November 14 remains a target, not a completion certificate. The full regression suite has not been run this session. Historical archive bytes, source permissions, original panel, and independently authenticated assignments remain unreconciled. Next: exact-checkout regression suite and authenticated event-time placebo/pretrend analysis with matched groups, security/exchange controls, common dates, and dependence-aware resampling. No causal interpretation is warranted.
