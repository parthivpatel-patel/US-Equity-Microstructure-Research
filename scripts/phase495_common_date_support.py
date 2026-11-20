"""Common-date support audit for eligibility panels; no causal estimator.

Requires date-specific eligibility and observations. All inputs remain unauthenticated
until separately matched to original SEC source records.
"""
from collections import defaultdict
from phase493_balanced_coverage import _read

def common_date_audit(eligibility, panel, cutoff):
    eligible = _read(eligibility, False)
    observed = _read(panel, True)
    if not eligible or set(observed) - set(eligible):
        raise ValueError("empty eligibility or out-of-universe observation")
    units = defaultdict(set)
    seen = defaultdict(set)
    for sec, ex, day in eligible:
        units[(sec, ex)].add(day)
    for sec, ex, day in observed:
        seen[(sec, ex)].add(day)
    paired = [u for u, days in units.items()
              if any(d < cutoff for d in days) and any(d >= cutoff for d in days)]
    full = [u for u in paired if units[u] == seen[u]]
    if not paired:
        raise ValueError("no two-sided eligible units")
    common_eligible = set.intersection(*(units[u] for u in paired))
    common_full = set.intersection(*(seen[u] for u in full)) if full else set()
    def sides(days):
        return {"pre": sum(d < cutoff for d in days),
                "post": sum(d >= cutoff for d in days)}
    return {"provenance_status": "UNAUTHENTICATED_INPUTS",
            "paired_eligible_units": len(paired),
            "fully_covered_paired_units": len(full),
            "common_eligible_dates_all_paired": sides(common_eligible),
            "common_observed_dates_all_full": sides(common_full),
            "common_eligible_dates": sorted(common_eligible),
            "common_full_dates": sorted(common_full),
            "warning": "Full unit coverage does not imply common-date balanced support."}
