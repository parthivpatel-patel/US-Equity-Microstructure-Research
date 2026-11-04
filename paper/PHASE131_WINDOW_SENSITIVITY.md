# Phase 131 — Event-window sensitivity and historical pseudo-events

Executed November 3, 2026 on the inherited Phase 130 processed panel (14,416 records, 68 matched groups, 106 trading dates, two outcomes). This is **exploratory** and is not independently authenticated to raw SEC or historical Nasdaq treatment data.

Each estimate is the equally weighted average of 68 matched-group changes: mean of W trading days beginning at candidate date minus mean of preceding W trading days. A historical pseudo-event qualifies only if the full post-window ends before November 3, 2025. The October 6 event is a previously selected diagnostic, not a prespecified control.

| Outcome | W | Nov. 3 (pp) | Oct. 6 (pp) | Nov. minus Oct. (pp) | Prior pseudo-events at least as negative | Eligible prior windows |
|---|---:|---:|---:|---:|---:|---:|
| Count | 3 | -1.171172 | -0.488827 | -0.682345 | 4 | 82 |
| Count | 5 | -1.335781 | -0.601120 | -0.734661 | 2 | 78 |
| Count | 7 | -1.039925 | -0.917497 | -0.122428 | 8 | 74 |
| Count | 10 | -1.143430 | -1.480595 | +0.337165 | 15 | 68 |
| Count | 15 | -2.100446 | -1.982149 | -0.118296 | 3 | 58 |
| Volume | 3 | -0.192894 | -0.394812 | +0.201918 | 36 | 82 |
| Volume | 5 | -0.006939 | -0.633537 | +0.626598 | 48 | 78 |
| Volume | 7 | +0.089135 | -0.898118 | +0.987253 | 52 | 74 |
| Volume | 10 | -0.240666 | -1.397351 | +1.156684 | 33 | 68 |
| Volume | 15 | -1.137118 | -1.855347 | +0.718230 | 9 | 58 |

**New result:** The November-minus-October count contrast reverses sign at the 10-day window (+0.337 pp), whereas the five-day contrast is negative (-0.735 pp). The count event's relative historical rank is also sensitive to window length. This is additional evidence that a headline five-day contrast is not robust to reasonable alternative windows. The volume November-minus-October contrast remains positive for all five windows.

The historical windows overlap, the October comparator was selected after inspection, and this scan is not multiplicity-adjusted. Counts are descriptive rankings, **not p-values**. There is no causal claim. Full source reconciliation, treatment authentication, venue-level controls, and joint matched-group/common-date inference remain open.

Reproduce with the exact processed input in the recovered Phase 130 ZIP and the independent Phase 131 script. The compact CSV below is published as a verified output; the underlying input and script are available in the local reproducibility package but are not yet confirmed uploaded to GitHub.
