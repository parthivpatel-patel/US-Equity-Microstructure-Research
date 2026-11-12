# Phase 318 — What the frozen placebo summaries do not identify (2026-11-12)

## Inputs and method

Read the published `results/phase130_summary.csv` through the connected GitHub integration, independently of the earlier Phase 317 narrative. Let `L = #{x <= d}` be the reported at-least-as-negative count, `A = #{|x| >= |d|}` the reported absolute-extreme count, and `R = #{x >= d}` the unreported right-tail count. The bounds below follow from set inclusion, without assuming independence, exchangeability, a particular empirical distribution, or absence of ties.

For `d > 0`, negative extreme observations are in L, so `max(0, A-L) <= R <= A`. For `d < 0`, every observation strictly greater than d is in R, so `n-L <= R <= n`. These are conservative logical bounds, not a calibrated sampling interval; ties prevent a sharper inference from these aggregates.

| Outcome | Event contrast (pp) | L | A | n | Logically admissible R |
| --- | ---: | ---: | ---: | ---: | ---: |
| Count | -0.7346606598677254 | 2 | 2 | 78 | 76 to 78 |
| Volume | +0.626597999820323 | 48 | 76 | 78 | 28 to 76 |

The volume right-tail frequency is **not identified** by the published lower-tail and absolute-extreme counts. In particular, the previously reported difference `76 - 48 = 28` is merely a lower bound on the right-tail count, **not** an estimate of it. Even the count right-tail range is not a test of a negative reform effect: the direction is reversed and the placebo windows overlap.

## Verification and scope

Five synthetic-fixture unit tests passed locally for the same bound logic (including the two published aggregate values). Reproduce on the published checkout:

```bash
python -m unittest discover -s tests -p 'test_phase318_placebo_identifiability.py'
python -m scripts.phase318_placebo_identifiability results/phase130_summary.csv
```

This is an exact aggregate-level partial-identification result, **not** a new empirical SEC panel estimate. No authenticated source observations, historical treatment labels, or underlying 78 placebo-window values were available to this phase. The October 2025 announcement/placebo warning, September pretrends, matched-group selection, weighting sensitivity, exchange/security effects and common-date/serial dependence remain unresolved. These descriptive counts must not be presented as p-values. The November 14 publication target remains conditional; a fully validated paper cannot yet be certified. Historical ZIP archives remain inaccessible for item-level licensing and provenance checks.
