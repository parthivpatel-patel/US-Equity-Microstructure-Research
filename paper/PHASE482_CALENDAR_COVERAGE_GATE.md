# Phase 482 — Calendar-anchored coverage and composition gate

2026-11-19. Adds an independently supplied trading-calendar gate and fixed security-exchange union grid, extending Phase 481. This is a **data-quality instrument**, not historical SEC analysis. No source data, treatment classifications, or causal claims are bundled.

The script requires a sorted, unique ISO-date calendar, rejects panel rows outside that calendar, duplicate security-date-exchange keys, nonfinite values and invalid cutoffs. It reports observed zeros separately from absent union-grid cells, plus four coverage categories: complete in both periods, pre only, post only, or incomplete in both. Pre/post completeness is defined relative to the supplied calendar, not observed dates alone.

**Limitations:** Calendar provenance is not authenticated by the script; union units exclude never-observed securities; source and treatment authentication remain external requirements. This is not an estimator, does not correct missing-not-at-random selection, and cannot resolve the October 2025 placebo or September pretrends without historical inputs.

Reproduce: `python scripts/phase482_calendar_audit.py PANEL.csv CALENDAR.csv 2025-10-01` (choose an interior date actually present in the calendar). Tests: `python -m unittest discover -s tests -p 'test_phase482_calendar_audit.py' -v`.

**Validation scope:** A locally executed precursor implementation passed six targeted tests, but the published refactor requires independent CI or checkout execution; do not infer that the entire repository passed. The November 14 manuscript deadline was missed; publication is not certified. Historical Phase 430/436 archives and Phase 472 executable artifacts remain outstanding.
