# Phase 406 — Pilot session-calendar falsification gate (2026-11-16)

## Independent calendar calculation

A local Python calendar enumeration finds **23 weekdays in October 2025** and **20 weekdays in November 2025 through November 28**. Excluding **Thursday November 27 (US Thanksgiving)** leaves **19 expected November trading sessions**, or **42 expected sessions** across the two months. The previously recovered pilot audit reported **23 October and 19 November observed dates**, so the **monthly counts agree** with this explicit calendar expectation.

**This is a count-level cross-check, not a newly executed audit of the underlying pilot file.** Equal monthly counts do not prove exact date membership: a missing trading session and an extra closed-day record could offset each other. The newly added `scripts/phase406_calendar_membership.py` tests exact date sets, date/tier duplicates, and three-tier completeness when run against the recovered source file. The source file was not available for execution in this session, so **calendar-membership pass is not claimed**. The code is independently testable, and a future run must execute it against the SHA-256-identified pilot source.

The scoped calendar includes October 13 (Columbus Day, equity markets open) and November 11 (Veterans Day, equity markets open); November 28 is treated as a trading session despite its early close. Only the explicitly specified October–November 2025 period is supported. Confirm this manually encoded expectation against official exchange schedules before certifying data coverage.

## Identification implications

A calendar pass would establish neither original SEC provenance nor completeness of individual security/exchange records. It would not authenticate lot assignments, supply September pretrends or matched controls, or resolve the substantial October placebo. Pilot aggregates must remain descriptive, with no causal claims.

## Reproduction

```sh
python scripts/phase406_calendar_membership.py /authorized/path/roundlot_pilot_daily.csv
```

Expected date count: 42; actual pass/fail is intentionally unreported until the original file is run. Source CSV remains unpublished pending provenance and redistribution permission. The November 14 deadline was missed; November 30 remains provisional, not certified.
