"""Recompute archived normal-reference HC3 p-values and intervals; not valid panel inference."""
import csv, math, sys
from statistics import NormalDist
Z95 = NormalDist().inv_cdf(.975)
def audit(path):
    with open(path, newline="", encoding="utf-8") as f: rows=list(csv.DictReader(f))
    fields={"outcome","specification","n_securities","n_treated","effect","se_HC3","p","ci_low","ci_high"}
    if not rows or not fields.issubset(rows[0]): raise ValueError("Missing columns or rows")
    seen=set(); out=[]
    for r in rows:
        key=(r["outcome"],r["specification"])
        if key in seen: raise ValueError("Duplicate outcome/specification")
        seen.add(key)
        n,t=int(r["n_securities"]),int(r["n_treated"])
        b,se,p,lo,hi=(float(r[k]) for k in ("effect","se_HC3","p","ci_low","ci_high"))
        if not all(map(math.isfinite,(b,se,p,lo,hi))) or not (0<t<n and se>0 and 0<=p<=1 and lo<hi): raise ValueError("Invalid row")
        expected_p=math.erfc(abs(b/se)/math.sqrt(2))
        p_error=abs(p-expected_p)
        ci_error=max(abs(lo-(b-Z95*se)),abs(hi-(b+Z95*se)))
        if p_error>max(1e-12,1e-7*expected_p) or ci_error>1e-10: raise ValueError("Inconsistent normal p or CI: "+str(key))
        out.append(dict(outcome=key[0],specification=key[1],p_error=p_error,ci_error=ci_error,n_securities=n))
    return out
if __name__=="__main__":
    if len(sys.argv)!=2: raise SystemExit("Usage: phase429_inference_audit.py INPUT.csv")
    for r in audit(sys.argv[1]): print(r)
