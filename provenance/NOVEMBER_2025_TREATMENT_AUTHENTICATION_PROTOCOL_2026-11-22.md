# November 3, 2025 treatment authentication: primary-source protocol (2026-11-22)

**Evidence status:** Official operational rules verified from primary Nasdaq/UTP documentation; **no stock-level November 3 assignment authenticated**. This note is a source and identification protocol, not a reconstructed treatment roster.

## Official assignment rule and source hierarchy

UTP Vendor Alert #2025-10 (May 7, 2025) specifies that each NMS stock's round-lot tier for the first business day in November is determined by the **average closing price on its primary listing exchange over all September trading days**, not its October 31 close or a November snapshot. The published tiers are $0–$250: 100 shares; $250.01–$1,000: 40; $1,000.01–$10,000: 10; above $10,000: 1. The UTP SIP **Issue Symbol Directory (Category A, Type B)** disseminates assigned round-lot size each morning. Source: https://www.nasdaqtrader.com/TraderNews.aspx?id=UTP2025-10

A later UTP reminder explicitly calls May 1, 2026 the **first reassignment since implementation**, reinforcing the distinction between the initial November 2025 assignments and later snapshots: https://www.nasdaqtrader.com/TraderNews.aspx?id=UTP2026-12 . This reminder does not supply November 2025 stock-level values.

**Preferred evidence (highest to lowest):** (1) actual November 3, 2025 production SIP issue-directory message with stock identifier and round-lot size, retaining feed/date provenance; (2) primary-listing-exchange historical official round-lot directory valid on November 3; (3) independently reconstructed September 2025 average of primary-exchange closing prices with contemporaneous symbol and corporate-action history; (4) late-October/November third-party listing snapshots, marked provisional. Never substitute August/September UTP **test broadcast** symbols for production assignments; UTP Vendor Alert #2025-20 documents that testing used designated test symbols and that a test symbol was removed following delisting: https://beta.nasdaqtrader.com/TraderNews.aspx?id=UTP2025-20

## Required treatment audit fields

For each security: stable security identifier; as-of-November-3 symbol; listing venue; all September primary-exchange close observations and count of eligible sessions; September arithmetic mean; corporate-action adjustment methodology; inferred tier and distance from threshold; original production directory tier if available; source URL/archive identifier, byte hash, and capture date; crosswalk flags (renamed, split, new listing, delisted, dual-class); and status **verified / reconstructed / provisional / unresolved**. Preserve contradictory sources rather than silently overwriting. Boundary cases require special review.

Define treated status only when the *effective* November 3 round lot is below the relevant prior round lot, and separately report exclusions for missing historical identifiers or incomplete September observations. A post-event listing snapshot can be a cross-check but not a substitute for the effective-date roster. Verify that all 68 provisionally treated names have eligible November 3 identifiers before treating 68 as a final cohort count.

## Consequence for the empirical design

The November 3 SIP change also reexpressed quote size in **actual shares** rather than units of round lots, affecting displayed quotation interpretation across securities. The reform cannot be modeled as only a binary stock-specific change without considering common market-wide implementation and venue effects. Hidden-execution metrics and their denominator definitions must be reconstructed independently from original SEC daily files; this source note certifies neither those inputs nor a causal effect.

**Unresolved:** original SEC Q3/Q4 ZIP bytes and hashes, production Nov-3 directory or equivalent historical roster, September-close reconstruction, daily placebo/pretrend analysis and clustered/bootstrap inference. No original data or third-party licensed content is redistributed here.
