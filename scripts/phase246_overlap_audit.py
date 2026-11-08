"""Audit dependence induced by overlapping fixed-width placebo windows.

Structural diagnostics only: no empirical p-values or causal claims.
"""

def audit_placebo_overlap(cuts, half_window, n_sessions):
    if type(half_window) is not int or half_window < 1:
        raise ValueError('half_window must be a positive integer')
    if type(n_sessions) is not int or n_sessions < 2 * half_window:
        raise ValueError('insufficient session count')
    if not isinstance(cuts, (list, tuple)) or not cuts or any(type(c) is not int for c in cuts):
        raise ValueError('cuts must be a nonempty integer sequence')
    if list(cuts) != sorted(set(cuts)):
        raise ValueError('cuts must be strictly increasing and unique')
    if any(c < half_window or c + half_window > n_sessions for c in cuts):
        raise ValueError('incomplete placebo window')
    windows = [(c - half_window, c + half_window) for c in cuts]
    pairs = []
    for i, (a, b) in enumerate(windows):
        for j in range(i + 1, len(windows)):
            x, y = windows[j]
            shared = max(0, min(b, y) - max(a, x))
            if shared:
                pairs.append({'first_cut': cuts[i], 'second_cut': cuts[j],
                              'shared_sessions': shared,
                              'fraction_of_each_window': shared / (2 * half_window)})
    independent_spacing_subset = []
    last_end = -1
    for cut, (start, end) in zip(cuts, windows):
        if start >= last_end:
            independent_spacing_subset.append(cut)
            last_end = end
    return {'n_cuts': len(cuts), 'n_overlapping_pairs': len(pairs),
            'overlapping_pairs': pairs,
            'nonoverlapping_cut_subset': independent_spacing_subset,
            'note': 'Disjoint windows do not guarantee statistically independent outcomes; common shocks and serial dependence may persist.'}
