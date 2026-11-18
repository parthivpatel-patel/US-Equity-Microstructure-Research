"""Calendar-only placebo overlap audit. Not an exchange-session calendar."""
from datetime import date

def audit(boundaries, reform="2025-11-03", earliest="2025-07-01", min_pre=10, min_post=10):
    r=date.fromisoformat(reform); start=date.fromisoformat(earliest)
    cuts=[date.fromisoformat(x) for x in boundaries]
    if not cuts or len(cuts)!=len(set(cuts)) or any(not start<c<r for c in cuts):
        raise ValueError("invalid or duplicate placebo dates")
    if type(min_pre) is not int or type(min_post) is not int or min_pre<1 or min_post<1:
        raise ValueError("invalid minimum windows")
    out=[]
    for c in sorted(cuts):
        pre=(c-start).days; post=(r-c).days
        out.append({"cutoff":c.isoformat(),"pre_calendar_days":pre,"post_calendar_days":post,
                    "passes_calendar_upper_bound":pre>=min_pre and post>=min_post})
    pairs=[]
    for i,a in enumerate(sorted(cuts)):
        for b in sorted(cuts)[i+1:]:
            pairs.append({"first":a.isoformat(),"second":b.isoformat(),
                          "days_reassigned_from_post_to_pre":(b-a).days,
                          "shared_total_window_days":(r-start).days})
    return {"windows":out,"pairs":pairs,"calendar_not_authenticated":True,
            "multiple_placebos_not_independent":True,
            "warning":"Calendar-day counts are not exchange-session counts; overlapping placebo tests are dependent."}
