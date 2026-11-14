# Phase 369 — Dated placebo calendar integrity gate

Date: 2026-11-14. **Software audit only; no authenticated SEC observations processed.**

Prior phases demonstrated that overlapping pseudo-event windows are dependent under independent and AR(1) daily shocks. A prerequisite for applying those results to the archived 78 pseudo-events is to recover their actual dates and an authenticated trading-session calendar. This phase supplies a strict, deterministic audit of the calendar mapping. It requires unique ascending session dates, unique event dates, event membership in the supplied session calendar, and complete pre/post windows; it enumerates the sessions on each side and all overlapping event-window pairs with their shared-session counts.

The implementation deliberately does **not** substitute weekdays for actual trading sessions, fabricate missing pseudo-event dates, estimate SEC effects, or produce calibrated p-values. With half-window five, constructed event indices 5 and 6 share nine of ten sessions; event index 16 has no overlap with either. These are fixture results, not market estimates.

Local verification: six focused Python unittest cases passed after correcting a prototype fixture that unintentionally had one-session overlap. Reproduce with `PYTHONPATH=scripts python -m unittest discover -s tests -p 'test_phase369_placebo_calendar.py' -v`. Published checkout and full repository suite remain untested.

To run on historical evidence, first authenticate the SEC source bytes and actual market-session calendar, recover all 78 dated pseudo-event definitions and their selection rule, verify treatment and matching, and reconcile the substantial October placebo and September pretrends. Then calculate observed overlap structure, common-date/serial dependence and sensitivity across estimands. No source archive has been imported in this phase. **November 14 publication deadline missed; manuscript uncertified; no causal claim.**
