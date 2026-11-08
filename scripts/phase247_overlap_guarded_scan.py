"""Add overlap diagnostics to guarded descriptive placebo scans.

No source, calendar, or treatment authentication is implied.
"""
from phase244_guarded_placebo import guarded_placebo_scan
from phase246_overlap_audit import audit_placebo_overlap


def overlap_guarded_placebo_scan(daily, cuts, half_window, bandwidth, *, admitted_sessions=None):
    """Run the existing guarded estimator, then annotate shared observation windows."""
    result = guarded_placebo_scan(daily, cuts, half_window, bandwidth,
                                  admitted_sessions=admitted_sessions)
    overlap = audit_placebo_overlap(cuts, half_window, len(daily))
    if len(result['results']) != overlap['n_cuts']:
        raise RuntimeError('placebo result count does not match overlap audit')
    result['overlap_audit'] = overlap
    result['multiplicity_adjusted'] = False
    result['serial_dependence_fully_addressed'] = False
    result['warning'] = (result['warning'] + ' Overlap is quantified, not statistically '
                         'corrected; disjoint windows can remain dependent.')
    return result
