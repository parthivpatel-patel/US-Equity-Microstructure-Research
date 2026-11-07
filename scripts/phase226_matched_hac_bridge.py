"""Bridge matched daily contrasts to full-series HAC; no source authentication."""
from phase225_matched_date_bootstrap import matched_daily
from phase224_common_date_hac import common_date_hac

def matched_full_series_hac(rows, pairs, sessions, exchanges, early_dates, late_dates, bandwidth):
    """Equal pair-exchange weighting, retaining covariance across the window boundary."""
    if list(sessions) != list(early_dates) + list(late_dates):
        raise ValueError('sessions must equal ordered windows')
    daily = matched_daily(rows, pairs, sessions, exchanges)
    transformed = [dict(date=r['date'], equal_cell_contrast=r['matched_contrast'],
                        pooled_count_contrast=r['matched_contrast']) for r in daily]
    result = common_date_hac(transformed, early_dates, late_dates, bandwidth)
    result.pop('pooled_count_contrast')
    result['weighting'] = 'equal pair-exchange cells; not pooled executions'
    result['pairs'] = len(pairs)
    result['exchanges'] = len(exchanges)
    result['security_cluster_inference'] = False
    return result
