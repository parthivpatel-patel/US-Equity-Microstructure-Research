"""Fixed-roster pair and date deletion sensitivity; descriptive only."""
from datetime import date
from math import isfinite

def audit(rows, cutoff):
    cut = date.fromisoformat(cutoff)
    cells = {}
    for r in rows:
        d = date.fromisoformat(r['date'])
        p = r['pair_id']
        if not isinstance(p, str) or not p or d.weekday() >= 5:
            raise ValueError('invalid pair or weekend; calendar not authenticated')
        a, b = r['treated'], r['control']
        if any(type(v) not in (int, float) or not isfinite(v) for v in (a, b)):
            raise ValueError('invalid outcome')
        if (d, p) in cells:
            raise ValueError('duplicate cell')
        cells[d, p] = a - b
    dates = sorted({d for d, _ in cells})
    pairs = sorted({p for _, p in cells})
    if len(pairs) < 2 or sum(d < cut for d in dates) < 2 or sum(d >= cut for d in dates) < 2:
        raise ValueError('need two pairs and two dates on each side')
    if len(cells) != len(dates) * len(pairs):
        raise ValueError('unbalanced panel')

    def estimate(ds, ps):
        pre = [cells[d, p] for d in ds if d < cut for p in ps]
        post = [cells[d, p] for d in ds if d >= cut for p in ps]
        return sum(post) / len(post) - sum(pre) / len(pre)

    full = estimate(dates, pairs)
    pair_deletions = {p: estimate(dates, [q for q in pairs if q != p]) for p in pairs}
    date_deletions = {d.isoformat(): estimate([e for e in dates if e != d], pairs) for d in dates}
    return {'full': full, 'leave_one_pair_out': pair_deletions,
            'leave_one_date_out': date_deletions,
            'max_pair_deletion_change': max(abs(v-full) for v in pair_deletions.values()),
            'max_date_deletion_change': max(abs(v-full) for v in date_deletions.values()),
            'n_pairs': len(pairs), 'n_dates': len(dates),
            'warning': 'synthetic/descriptive sensitivity only; no source or treatment authentication, no inference'}
