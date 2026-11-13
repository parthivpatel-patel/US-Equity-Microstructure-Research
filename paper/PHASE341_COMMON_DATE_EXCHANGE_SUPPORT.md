# Phase 341 — Matched-group calendar and exchange support gate (2026-11-13)

This standard-library diagnostic counts dates with both treatment arms present within each matched group and separately within each group–exchange pair. It complements Phase 340's structural gate. **No authenticated SEC observations were processed; no effect estimates or causal claims.**

Run `python scripts/phase341_support.py authorized_panel.csv` after Phase 340; run tests with `python -m unittest tests.test_phase341_support -v`. Eight local synthetic tests passed before publication using equivalent script logic (the local test harness imported its script from a temporary directory). A post-publication full checkout test is still required.

**Key identification distinction:** Same-date overlap at group level can coexist with *zero* same-date overlap within exchanges. Pooling across exchanges can therefore mask absent exchange-specific support. The diagnostic reports both levels without pretending exchange composition is balanced. Dates with only one treatment arm are also counted. The diagnostic does not impose a minimum coverage threshold, assess securities' weights, check trading-session completeness, or authenticate the provisional reform cohort.

**Publication gate:** Phase 130's five-day count placebo contradiction remains unresolved; September pretrends and the substantial October break are material; original 78 dated placebo contrasts, source files, treatment authentication, selection and weighting sensitivity, serial-dependence-aware joint inference, and historical ZIP provenance remain open. The November 14 manuscript target is not certified.

**Next:** Obtain authenticated security/date/exchange panel, execute Phases 340–341 and document zero-support strata, then reconstruct pretrend/placebo inference with common-date and matched-group dependence preserved. No licensed raw inputs are redistributed.
