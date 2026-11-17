"""Illustrative multiplicity audit of archived derived inference rows.

Usage: python scripts/phase427_multiplicity_audit.py archive/recovered_outputs/roundlot_phase2_inference_2026-10-27.csv
These adjustments are NOT validated inference: five hypotheses were not preregistered
as a family, and the underlying HC3 p-values may mishandle panel dependence.
"""
import csv
import math
import sys
from pathlib import Path


def audit(path):
    with Path(path).open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    if len(rows) != 5 or len({(r["outcome"], r["specification"]) for r in rows}) != 5:
        raise ValueError("Expected five distinct archived outcome/specification rows")
    for row in rows:
        for key in ("effect", "se_HC3", "p", "ci_low", "ci_high"):
            row[key] = float(row[key])
            if not math.isfinite(row[key]):
                raise ValueError(f"Nonfinite {key}")
        if row["se_HC3"] <= 0 or not 0 <= row["p"] <= 1:
            raise ValueError("Invalid standard error or p-value")
    ordered = sorted(rows, key=lambda row: row["p"])
    running = 0.0
    for index, row in enumerate(ordered):
        running = max(running, (len(rows) - index) * row["p"])
        row["holm_illustrative"] = min(1.0, running)
        row["bonferroni_illustrative"] = min(1.0, len(rows) * row["p"])
    return rows


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: phase427_multiplicity_audit.py INPUT.csv")
    for row in audit(sys.argv[1]):
        print(f'{row["outcome"]},{row["specification"]}: p={row["p"]:.10g}, '
              f'Holm={row["holm_illustrative"]:.10g}, '
              f'Bonferroni={row["bonferroni_illustrative"]:.10g}')
