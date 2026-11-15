# Phase 390 — original dated placebo record audit

Date: 2026-11-15. Independent round-lot reform study only.

This fail-closed CSV validator checks ISO placebo dates, declared inclusive windows, finite numerical estimates, explicit estimands, duplicate date/estimand/window keys, and syntactically valid source SHA-256 fields. It flags multiple nominal dates sharing an identical declared window, without treating those windows as independent. The SHA-256 of the input CSV is emitted for subsequent provenance reconciliation.

Run: `python scripts/phase390_placebo_record_gate.py /path/to/placebo_records.csv`. Required columns: `placebo_date,estimate,estimand,window_start,window_end,source_sha256`. No original dated placebo records were available for empirical execution. Nine constructed-fixture tests passed locally. No SEC observations were processed. A syntactically valid source hash does not authenticate its source; declared calendar windows do not verify effective trading-session windows. No causal or inferential conclusion follows.

Outstanding: original 78 dated placebo records, substantial October placebo warning, September pretrends, historical treatment authentication, selection/weighting sensitivity, matched-pair and common-date/serial dependence, source provenance and licensed archive recovery. November 14 publication target missed; manuscript remains uncertified.
