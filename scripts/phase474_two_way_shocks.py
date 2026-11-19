"""Exact balanced-panel placebo covariance under group/date/idiosyncratic shocks; synthetic only."""
import math

def covariance(n_dates, cutoffs, n_groups, group_loading=1.0, date_loading=1.0, noise_loading=1.0):
    if not isinstance(n_dates,int) or n_dates<3 or not isinstance(n_groups,int) or n_groups<2:
        raise ValueError('invalid panel dimensions')
    if not cutoffs or len(set(cutoffs)) != len(cutoffs) or any(not isinstance(k,int) or not 0<k<n_dates for k in cutoffs):
        raise ValueError('invalid cutoffs')
    if any(not math.isfinite(v) or v<0 for v in (group_loading,date_loading,noise_loading)):
        raise ValueError('invalid shock loadings')
    weights=[[-1/k if t<k else 1/(n_dates-k) for t in range(n_dates)] for k in cutoffs]
    # Time-invariant group shocks cancel in within-group pre/post contrasts.
    scale=date_loading**2+noise_loading**2/n_groups
    return [[scale*math.fsum(a*b for a,b in zip(w,v)) for v in weights] for w in weights]

def summary(n_dates=40,cutoffs=(10,20,30),n_groups=68,date_loading=1,noise_loading=1):
    c=covariance(n_dates,cutoffs,n_groups,date_loading=date_loading,noise_loading=noise_loading)
    iid=covariance(n_dates,cutoffs,n_groups,date_loading=0,noise_loading=noise_loading)
    return {'n_dates':n_dates,'n_groups':n_groups,'cutoffs':list(cutoffs),
            'date_loading':date_loading,'noise_loading':noise_loading,
            'covariance':c,'iid_only_covariance':iid,
            'se_inflation':[math.sqrt(c[i][i]/iid[i][i]) for i in range(len(c))]}
