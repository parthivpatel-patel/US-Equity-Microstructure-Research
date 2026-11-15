"""Audit shared-session dependence among eligible placebo windows; no empirical estimates."""
from itertools import combinations

def audit_placebo_overlap(calendar_audit):
    """Find duplicate effective windows and shared-session overlap components."""
    eligible = [r for r in calendar_audit['results'] if r['eligible']]
    boundaries = [r['boundary'] for r in eligible]
    if len(boundaries) != len(set(boundaries)):
        raise ValueError('duplicate eligible boundaries')
    windows = []
    for r in eligible:
        pre, post = tuple(r['pre']), tuple(r['post'])
        if not pre or not post or len(set(pre + post)) != len(pre) + len(post):
            raise ValueError('invalid or overlapping within-window sessions')
        if tuple(sorted(pre)) != pre or tuple(sorted(post)) != post or pre[-1] >= post[0]:
            raise ValueError('invalid session order')
        windows.append((pre, post))
    parent = list(range(len(eligible)))
    def root(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i
    def union(i, j):
        a, b = root(i), root(j)
        if a != b:
            parent[b] = a
    duplicates, overlaps = [], []
    for i, j in combinations(range(len(eligible)), 2):
        a, b = windows[i], windows[j]
        shared = sorted(set(a[0] + a[1]) & set(b[0] + b[1]))
        if a == b:
            duplicates.append((boundaries[i], boundaries[j]))
        if shared:
            overlaps.append({'a': boundaries[i], 'b': boundaries[j],
                             'shared_sessions': len(shared),
                             'union_sessions': len(set(a[0] + a[1] + b[0] + b[1]))})
            union(i, j)
    groups = {}
    for i, boundary in enumerate(boundaries):
        groups.setdefault(root(i), []).append(boundary)
    components = tuple(sorted((tuple(sorted(g)) for g in groups.values()), key=lambda x: x[0]))
    return {'eligible_boundaries': len(eligible), 'duplicate_window_pairs': tuple(duplicates),
            'overlapping_pairs': tuple(overlaps), 'overlap_components': components,
            'source_authenticated': False, 'independence_established': False}
