# Phase 266: Source byte integrity gate

This standard-library tool compares locally available files against an independently prepared SHA-256 and byte-size manifest. It rejects missing or mismatched files, duplicate paths, traversal, symlink escape, and malformed digests. A digest generated from an untrusted file and checked against that same file is **not** independent source authentication.

Run tests: `python -m unittest discover -s tests -p 'test_phase266_source_manifest.py' -v`.

Run audit: `python scripts/phase266_source_manifest.py --root /path/to/data --manifest /path/to/manifest.json`.

Manifest shape: `{"files":[{"path":"example.csv","size_bytes":123,"sha256":"0000000000000000000000000000000000000000000000000000000000000000"}]}` (placeholder, not real data).

Byte integrity, source authentication, treatment authentication, and inference authorization are separate. The last three remain false by design. Independently authenticate SEC issuer, version, acquisition timestamp, license, data definitions, and immutable expected hashes; authenticate exchange trading dates and round-lot assignments using applicable rules and reference prices. Freeze security/exchange matched roster, audit September pretrends and substantial October placebo, report selection and weighting sensitivity, and use common-date plus serial/cross-sectional dependence-aware inference before causal interpretation.

No historical SEC data were analyzed, no historical coefficients or figures were generated, and no historical ZIPs or unpublished older scripts were imported in this phase. Historical archives, independent digest attestations, treatment classifications, and license permissions remain unverified. No causal effect is established.
