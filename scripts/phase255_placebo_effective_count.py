"""Exact combinatorial diagnostics for equally wide placebo windows.

Does not estimate statistical effective sample size or independence.
"""

def overlap_components(cuts, half_window, n_sessions):
    if type(half_window) is not int or half_window < 1:
        raise ValueError('half_window must be a positive integer')
    if type(n_sessions) is not int or n_sessions < 2 * half_window:
        raise ValueError('invalid session count')
    if not isinstance(cuts, (tuple, list)) or not cuts or any(type(c) is not int for c in cuts):
        raise ValueError('invalid cuts')
    if list(cuts) != sorted(set(cuts)):
        raise ValueError('cuts must be strictly increasing')
    if cuts[0] < half_window or cuts[-1] + half_window > n_sessions:
        raise ValueError('incomplete windows')
    components = []
    current = [cuts[0]]
    for cut in cuts[1:]:
        if cut - current[-1] < 2 * half_window:
            current.append(cut)
        else:
            components.append(current)
            current = [cut]
    components.append(current)
    selected = []
    for cut in cuts:
        if not selected or cut - selected[-1] >= 2 * half_window:
            selected.append(cut)
    return {'candidate_cuts': len(cuts), 'overlap_components': components,
            'component_count': len(components), 'max_disjoint_windows': len(selected),
            'greedy_disjoint_cuts': selected,
            'interpretation': 'Combinatorial window counts only; not independent tests or effective statistical sample size.'}
