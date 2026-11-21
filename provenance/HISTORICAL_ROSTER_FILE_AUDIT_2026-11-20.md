# Historical round-lot roster provenance audit — 2026-11-20

**Status:** newly recovered *local* historical-looking NYSE listing-venue file, and an unusable later-dated Nasdaq file. **No original-feed authenticity claim.**

## Recovered materials and byte hashes

Two previously unexamined files were located in the research file library, materialized as read-only research inputs and parsed locally:

- `NYSEGroupRLSymbolUpdates_20251031.txt` — 201,335 bytes; SHA-256 `40af12d8ddf73166330d54a96c2094f2f244c208e5bda0203567894a1f6822f4`. Six columns: Measurement Month, Trade Date, Symbol, Refsym, Listed Mic, Round Lot Size. All **5,666** records have Measurement Month **202509** and Trade Date **20251031**. **5,666 distinct symbols and reference symbols**; listed MIC distribution: XNYS 2,882; ARCX 2,486; XASE 298. Lot-size distribution: 1 share **1**, 10 shares **13**, 40 shares **156**, 100 shares **5,496**.
- `NasdaqListedRoundLotUpdates.txt` — 195,293 bytes; SHA-256 `844f0b46fc7aa9b735aa8c033c3f97fffe85b9507bb26b6f64b40597afef8b99`. Contains **5,636 rows explicitly labeled evaluation_period 202609**, and **one trailing non-data timestamp row**. **Zero** rows labeled September 2025. **Must not be used** to authenticate 2025 reform treatment assignments.

Both were retrieved from the user's saved file library, **not independently downloaded from NYSE or Nasdaq** in this run. Dates are internal file fields, not authenticated vendor provenance. Raw symbol lists are **not** uploaded to the public repository pending source/license and authenticity review.

## Comparison with recovered study panel

Compared all 2,262 tickers (68 provisionally treated) in `roundlot_phase2_security_panel.csv` (SHA-256 `2ccb80427a765ca3858f11f2874d6f87a79a559ec1fdeafc34420e82840e5bbb`) against the 5,666 NYSE-file listing symbols. **Zero ticker overlap**, including **zero** of the 68 treated names. This is consistent with the Phase 2 panel being assembled from Nasdaq-listed symbols and the NYSE file describing NYSE Group listings. It is **not** a validation failure for either source; it means the NYSE file cannot validate this Nasdaq-listed treatment cohort by direct ticker intersection.

The NYSE historical file is potentially useful as an *independent, differently listed* universe for future extension, subject to source authentication and identifier crosswalk. It is **not** evidence that the study's 68 assignments were correct. Do not conflate the 2026 Nasdaq file with 2025 historical data.

## Reproduction and checks

`python scripts/historical_roster_audit.py /path/to/NYSEGroupRLSymbolUpdates_20251031.txt /path/to/NasdaqListedRoundLotUpdates.txt /path/to/roundlot_phase2_security_panel.csv`

`python -m unittest discover -s tests -p test_historical_roster_audit.py -v`

**8/8** local deterministic tests passed (0.010 seconds). The script validates header/schema, measurement-month and trade-date consistency, unique NYSE symbols and reference identifiers, lot-size categories, and panel treatment labels. It writes aggregate counts and input SHA-256s, never raw proprietary listing rows. The tests use constructed fixtures; the published aggregate JSON was computed from actual recovered library files. The published checkout was **not** separately executed in this session.

## Critical blockers and next actions

1. Authenticate the original source/receipt and effective-date semantics of the NYSE historical file; its filename and date columns alone are insufficient.
2. Locate a **September 2025** Nasdaq-listed production round-lot directory or independently reproduce September average closing-price thresholds and corporate-action adjustments. The available 2026 Nasdaq file cannot be substituted.
3. Retrieve SEC Q3/Q4 2025 individual-security/exchange ZIPs and record original SHA-256s. A direct SEC HTTP request from the local runtime failed with a DNS NameResolutionError this session; no source ZIP was downloaded.
4. Reconcile matched cohort, September pretrend and October placebo on authenticated common dates and venues with dependence-aware inference.

Original 2026-11-14 deadline missed. This is a **provenance discovery**, not a treatment-authentication success, new causal effect, or completed paper. Independent of GIG and all other projects.
