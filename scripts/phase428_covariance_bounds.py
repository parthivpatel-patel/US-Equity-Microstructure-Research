"""Covariance-feasibility audit of archived paired-specification estimates.

This is an algebraic diagnostic, NOT validated inference. HC3 standard errors
may fail under date, exchange, security and serial dependence.
Usage: python scripts/phase428_covariance_bounds.py archive/recovered_outputs/roundlot_phase2_inference_2026-10-27.csv
"""
import csv
import math
import sys

def bounds(path):
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    results = []
    for outcome in ("dr", "dv"):
        selected = [r for r in rows if r["outcome"] == outcome]
        by_spec = {r["specification"]: r for r in selected}
        if len(selected) != 2 or set(by_spec) != {"unadjusted", "baseline_adjusted"}:
            raise ValueError("Missing or duplicate paired specification for " + outcome)
        a, b = by_spec["unadjusted"], by_spec["baseline_adjusted"]
        if (a["n_securities"], a["n_treated"]) != (b["n_securities"], b["n_treated"]):
            raise ValueError("Different reported sample counts")
        x, y = float(a["effect"]), float(b["effect"])
        sx, sy = float(a["se_HC3"]), float(b["se_HC3"])
        if not all(map(math.isfinite, (x, y, sx, sy))) or min(sx, sy) <= 0:
            raise ValueError("Nonfinite effect or invalid SE")
        delta = y - x
        se_min, se_max = abs(sx - sy), sx + sy
        results.append({"outcome": outcome, "delta": delta,
                        "se_min": se_min, "se_max": se_max,
                        "min_abs_z": abs(delta) / se_max,
                        "max_abs_z": abs(delta) / se_min if se_min else math.inf,
                        "same_counts_not_same_observations": True})
    return results

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: phase428_covariance_bounds.py INPUT.csv")
    for r in bounds(sys.argv[1]):
        print(f'{r["outcome"]}: adjusted-minus-unadjusted={r["delta"]:.12f}; '
              f'feasible SE=[{r["se_min"]:.12f},{r["se_max"]:.12f}]; '
              f'illustrative |z|=[{r["min_abs_z"]:.6f},{r["max_abs_z"]:.6f}]')
