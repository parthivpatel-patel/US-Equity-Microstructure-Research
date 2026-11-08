"""Prespecified common-date placebo cut scan; descriptive only, no source authentication."""
from phase224_common_date_hac import common_date_hac

def placebo_scan(daily, cuts, half_window, bandwidth):
    """Compare exactly half_window sessions on either side of each cut index."""
    if not isinstance(daily, list) or not daily:
        raise ValueError('nonempty daily panel required')
    if type(half_window) is not int or half_window < 2:
        raise ValueError('half_window must be an integer >=2')
    if type(bandwidth) is not int or bandwidth < 0 or bandwidth >= 2*half_window:
        raise ValueError('invalid bandwidth')
    if not isinstance(cuts, (list, tuple)) or not cuts or any(type(c) is not int for c in cuts):
        raise ValueError('integer cut indices required')
    if list(cuts) != sorted(set(cuts)):
        raise ValueError('cuts must be sorted and unique')
    dates = [r.get('date') for r in daily]
    if len(set(dates)) != len(dates) or dates != sorted(dates):
        raise ValueError('daily dates must be sorted and unique')
    if any(c < half_window or c + half_window > len(daily) for c in cuts):
        raise ValueError('cut lacks complete symmetric window')
    results = []
    for c in cuts:
        window = daily[c-half_window:c+half_window]
        early = dates[c-half_window:c]
        late = dates[c:c+half_window]
        estimate = common_date_hac(window, early, late, bandwidth)
        results.append({'cut_date':dates[c], 'early_start':early[0], 'late_end':late[-1],
                        'equal_cell_difference':estimate['equal_cell_contrast']['difference'],
                        'equal_cell_hac_se':estimate['equal_cell_contrast']['hac_se'],
                        'pooled_count_difference':estimate['pooled_count_contrast']['difference'],
                        'pooled_count_hac_se':estimate['pooled_count_contrast']['hac_se']})
    return {'results':results, 'half_window':half_window, 'bandwidth':bandwidth,
            'source_authenticated':False, 'treatment_authenticated':False,
            'calendar_independently_verified':False, 'causal_effect_established':False,
            'warning':'Exploratory descriptive placebo scan. Overlapping windows and cut selection invalidate naive independent-test interpretations.'}
