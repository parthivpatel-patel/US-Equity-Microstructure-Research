# Phase 393 — bounded ZIP member verification (2026-11-15)

This session extends [Phase 392](../scripts/phase392_archive_inventory.py) from untrusted ZIP directory metadata to **actual decompression and CRC-checked member bytes**, without extracting anything to disk. The verifier preflights duplicate names, absolute/traversal paths, symlinks, encrypted entries, member counts, declared sizes and compression ratios, then streams each member with hard actual-byte limits and SHA-256. Its output explicitly refuses source-authentication, redistribution and safe-extraction certification.

## Verification and interpretation

Ten deterministic local tests passed on constructed ZIP fixtures, including deliberately corrupted stored-member bytes that trigger a CRC rejection, path traversal, duplicate names, aggregate/member limits and SHA-256 verification. These are software tests, **not** SEC empirical observations. The exact published checkout and full repository suite remain untested. The original historical ZIPs were not available in this session and none were imported.

**Reproducible command:** `python -m unittest discover -s tests -p 'test_phase393_zip_member_verify.py'`; `python scripts/phase393_zip_member_verify.py /path/to/authorized.zip`.

**Scientific status:** November 14 publication target missed; manuscript uncertified. October 2025 placebo warning, September pretrends, 78 dated placebo estimates, treatment authentication, weighting/selection robustness and joint serial/date/matched-pair inference are still unresolved. Passing archive checks never validates a causal claim. Next: recover authorized original archives, reconcile source hashes, and rerun the pretrend/placebo analysis on authenticated observations.
