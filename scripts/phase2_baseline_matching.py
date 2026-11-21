#!/usr/bin/env python3
"""Descriptive baseline nearest-neighbor matching of an archived processed stock panel.

NOT a causal estimator or authenticated SEC-source analysis.
Usage: python scripts/phase2_baseline_matching.py path/to/roundlot_phase2_security_panel.csv
"""
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.spatial import cKDTree

EXPECTED_SHA = "2ccb80427a765ca3858f11f2874d6f87a79a559ec1fdeafc34420e82840e5bbb"

def analyze(path):
    raw = Path(path).read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if digest != EXPECTED_SHA:
        raise ValueError("Archived processed input SHA-256 differs; refusing silent substitution")
    d = pd.read_csv(path)
    if len(d) != 2262 or d.Ticker.duplicated().any() or d.treated.sum() != 68:
        raise ValueError("Archived panel membership or uniqueness changed")
    features = ["r_pre", "v_pre", "log_trades_pre"]
    d["log_trades_pre"] = np.log1p(d.trades_pre)
    if not (d.trades_pre > 0).all() or not np.isfinite(d[features+["dr","dv"]]).all().all():
        raise ValueError("Invalid numeric inputs")
    t = d[d.treated == 1].reset_index(drop=True)
    c = d[d.treated == 0].reset_index(drop=True)
    sd = d[features].std(ddof=1).to_numpy()
    tx = t[features].to_numpy() / sd
    cx = c[features].to_numpy() / sd
    tree = cKDTree(cx)
    def gap(col, weights=None):
        return float(t[col].mean() - (c[col].mean() if weights is None else np.average(c[col], weights=weights)))
    out = {
        "input_sha256": digest,
        "source_authentication": "NOT VERIFIED",
        "treated": len(t), "controls": len(c),
        "method": "Euclidean nearest controls in pooled-SD standardized baseline hidden trade rate, hidden volume rate and log1p(pre-trades); replacement allowed",
        "unmatched_smd": {f:gap(f)/sd[i] for i,f in enumerate(features)},
        "unmatched_count_gap_pp": 100*gap("dr"),
        "unmatched_volume_gap_pp": 100*gap("dv"),
        "models": []
    }
    nearest = tree.query(tx,k=1)[0]
    out["treated_nearest_distance_gt_0_5"] = int((nearest > 0.5).sum())
    out["treated_nearest_distance_gt_1"] = int((nearest > 1).sum())
    for k in (1,3,5):
        dist, idx = tree.query(tx,k=k)
        if k == 1:
            dist, idx = dist[:,None], idx[:,None]
        counts = np.bincount(idx.ravel(),minlength=len(c))
        weights = counts/k
        out["models"].append({
            "k":k, "n_distinct_controls":int((counts>0).sum()),
            "max_control_reuse":int(counts.max()),
            "max_nearest_distance":float(dist[:,0].max()),
            "median_nearest_distance":float(np.median(dist[:,0])),
            "smd_after":{f:gap(f,weights)/sd[i] for i,f in enumerate(features)},
            "count_change_gap_pp":100*gap("dr",weights),
            "volume_change_gap_pp":100*gap("dv",weights)
        })
    return out

if __name__ == "__main__":
    print(json.dumps(analyze(sys.argv[1]),indent=2,sort_keys=True))
