"""Descriptive HAC bandwidth sensitivity on authenticated-input candidates only.

No historical source or treatment authentication is performed here.
"""
from phase224_common_date_hac import common_date_hac

def bandwidth_sensitivity(daily, early_dates, late_dates, bandwidths):
    if not isinstance(bandwidths, (list, tuple)) or not bandwidths:
        raise ValueError("nonempty bandwidth list required")
    if any(type(b) is not int or b < 0 for b in bandwidths):
        raise ValueError("bandwidths must be nonnegative integers")
    if len(set(bandwidths)) != len(bandwidths) or list(bandwidths) != sorted(bandwidths):
        raise ValueError("bandwidths must be unique and sorted")
    n = len(early_dates) + len(late_dates)
    if any(b >= n for b in bandwidths):
        raise ValueError("bandwidth must be smaller than sample")
    results = []
    for b in bandwidths:
        estimate = common_date_hac(daily, early_dates, late_dates, b)
        results.append({
            "bandwidth": b,
            "early_n": estimate["early_n"],
            "late_n": estimate["late_n"],
            "equal_cell_contrast": estimate["equal_cell_contrast"],
            "pooled_count_contrast": estimate["pooled_count_contrast"],
        })
    return {
        "results": results,
        "source_authenticated": False,
        "calendar_independently_verified": False,
        "treatment_authenticated": False,
        "causal_effect_established": False,
        "warning": "Bandwidth sensitivity is descriptive; zero standard errors in small or constant fixtures do not imply certainty.",
    }
