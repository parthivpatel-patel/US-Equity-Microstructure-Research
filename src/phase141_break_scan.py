"""Phase 141: descriptive 20-day local slope-break scan; not causal inference.
Run from a directory containing phase131/daily_group_contrasts.csv.
"""
import hashlib
from pathlib import Path
import numpy as np
import pandas as pd
p = Path("phase131/daily_group_contrasts.csv")
assert hashlib.sha256(p.read_bytes()).hexdigest() == "6347d66cd7fa7ffa070b60529935e7ca9c93ef5c7f8dc61050fba33582f9aea1"
df = pd.read_csv(p, parse_dates=["date"])
assert len(df) == 14416 and df.group.nunique() == 68 and df.date.nunique() == 106
assert not df.duplicated(["group", "date", "outcome"]).any()
assert df.contrast.notna().all()
pre = df[df.date < "2025-11-03"]
rows = []
for outcome, sub in pre.groupby("outcome"):
    wide = sub.pivot(index="date", columns="group", values="contrast").sort_index()
    assert wide.notna().all().all()
    y = wide.mean(axis=1).to_numpy()
    dates = wide.index
    for i in range(20, len(y)-19):
        before = np.polyfit(np.arange(20), y[i-20:i], 1)[0]
        after = np.polyfit(np.arange(20), y[i:i+20], 1)[0]
        rows.append(dict(outcome=outcome, break_date=str(dates[i].date()),
                         pre_slope=before, post_slope=after,
                         shift=after-before, abs_shift=abs(after-before)))
result = pd.DataFrame(rows)
result.to_csv("phase141_break_scan.csv", index=False, float_format="%.12g")
for outcome, group in result.groupby("outcome"):
    print(outcome, "candidates", len(group))
    print("October 1", group[group.break_date=="2025-10-01"][["shift","abs_shift"]].to_string(index=False))
    print(group.nlargest(5, "abs_shift")[["break_date","shift"]].to_string(index=False))
