# Phase 340 — Raw panel structural-integrity gate (2026-11-13)

## Contribution
Added a **standard-library-only, fail-closed panel validator** for future authenticated security × date × exchange input. Unlike Phases 330–339, which audit published aggregates, this checks individual observation structure before any estimation. It does **not** claim to have recovered the underlying SEC observations.

Required CSV fields: `security,date,exchange,hidden_count,trade_count,hidden_shares,total_shares,treated,match_group`. Optional `source_id` is informational only and does not authenticate data. Count/share columns must be finite nonnegative integers; hidden numerators cannot exceed their respective totals. Reject duplicate security-date-exchange keys, invalid dates, missing identifiers, and security-level treatment/match-group drift. Report groups missing either treated or control securities as a blocking result.

Run `python scripts/phase340_panel_integrity.py path/to/authorized_panel.csv`; exit 1 indicates blocked structural integrity. Run `PYTHONPATH=scripts python -m unittest discover -s tests -p 'test_phase340_panel_integrity.py' -v`. Ten tests passed locally on 2026-11-13, including four invalid numeric fixtures. No actual SEC observations were processed. This is a preparatory data-quality gate, **not** an analysis of pretrends, placebos, matched effects or inference.

## Interpretation and missing requirements
Structural checks do not authenticate source files, verify the 2025-11-03 treatment assignments, detect missing trading sessions, reconcile exchange reporting definitions, verify SEC measure semantics, or establish that matched controls are suitable. Match-group completeness does not prove adequate overlap, common-date support, or balanced weighting. No serial-dependence-aware inference is performed.

The October placebo warning, September pretrends, contradictory Phase 130 five-day hidden-count tails, unknown original 78 placebo observations, selection/weighting sensitivity, security/exchange controls, and historical archive inventory remain open. No causal claims. November 14 manuscript certification remains blocked.

## Next executable step
Locate legally redistributable or locally available authenticated security-date-exchange input and producing scripts; hash source artifacts, establish licensing and source definitions, run this structural gate, and then calculate coverage, date-support, placebo and dependence-aware diagnostics. Do not publish licensed underlying data or unverified graphics.
