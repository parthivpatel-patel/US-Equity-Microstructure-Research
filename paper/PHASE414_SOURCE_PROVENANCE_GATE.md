# Phase 414 — Local historical-source provenance gate

Date: 2026-11-16. Independent U.S. equity round-lot reform research only.

## Reproducible command
From repository root: `python -m unittest discover -s tests -p 'test_phase414_provenance_gate.py'`.
For local files: `python scripts/phase414_provenance_gate.py manifest.json --root /path/to/local/data`.

Manifest shape: `{"sources":[{"path":"relative.csv","sha256":"64 lowercase hex characters","source_url":"https://source.example/data","retrieved_utc":"2026-11-16T00:00:00Z","redistribution":"restricted","grain":"security-exchange-date"}]}`.

The gate checks mandatory provenance fields, SHA-256 file integrity, file presence, duplicate paths, and traversal outside the data root. Restricted or unknown redistribution rights do **not** authorize publication: the gate's PASS only means that local provenance metadata and hashes match. Licensing, source authenticity, treatment assignment, complete security/date coverage, and research identification require separate checks. Manifest metadata is supplied by the researcher and is not independently authenticated by this script.

Seven deterministic local tests passed on the initial standalone implementation. No historical SEC panel was available to run through this gate. The historical October placebo warning, September pretrends, treatment authentication, weighting/selection sensitivity, and dependence-aware inference remain unresolved. The November 14 publication deadline was missed; no publication certification is claimed.

Historical ZIPs, raw licensed files, and recovered matching assignments were not imported in this phase. The next step is to inventory recovered inputs and validate authentic hashes and permissions before empirical reuse.
