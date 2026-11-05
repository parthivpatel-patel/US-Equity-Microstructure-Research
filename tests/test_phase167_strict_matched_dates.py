"""Phase 167: strict matched-date integrity checks; constructed fixtures only."""
import math
import unittest

def paired_dates(rows, cutoff):
    cells = {}
    for d,g,a,y in rows:
        if not isinstance(d,str) or not d or not isinstance(g,str) or not g:
            raise ValueError("invalid identifiers")
        if type(a) is not int or a not in (0,1):
            raise ValueError("invalid arm")
        if isinstance(y,bool) or not isinstance(y,(int,float)) or not math.isfinite(y):
            raise ValueError("invalid outcome")
        k=(d,g,a)
        if k in cells: raise ValueError("duplicate cell")
        cells[k]=float(y)
    dates=sorted({d for d,g,a in cells})
    if not any(d<cutoff for d in dates) or not any(d>=cutoff for d in dates):
        raise ValueError("both periods required")
    groups=sorted({g for d,g,a in cells})
    pairs={(d,g):cells[d,g,1]-cells[d,g,0] for d in dates for g in groups
           if (d,g,0) in cells and (d,g,1) in cells}
    bydate={d:[pairs[d,g] for g in groups if (d,g) in pairs] for d in dates}
    if any(not x for x in bydate.values()): raise ValueError("date without pair")
    balanced=[g for g in groups if all((d,g) in pairs for d in dates)]
    return {"available":{d:sum(x)/len(x) for d,x in bydate.items()},
            "balanced":({d:sum(pairs[d,g] for g in balanced)/len(balanced)
                         for d in dates} if balanced else None),
            "pair_counts":{d:len(x) for d,x in bydate.items()},
            "balanced_groups":len(balanced),
            "incomplete_arms":sum(((d,g,0) in cells)!=((d,g,1) in cells)
                                   for d in dates for g in groups)}

class Tests(unittest.TestCase):
    def test_composition(self):
        rows=[(d,g,a,100+a*effect) for d in ("01","02","03","04")
              for g,effect in (("A",0),("B",10))
              if not (g=="B" and d in ("01","02")) for a in (0,1)]
        x=paired_dates(rows,"03")
        self.assertEqual(list(x["available"].values()),[0,0,5,5])
        self.assertEqual(list(x["balanced"].values()),[0,0,0,0])
        self.assertEqual(list(x["pair_counts"].values()),[1,1,2,2])
    def test_duplicate(self):
        with self.assertRaises(ValueError):
            paired_dates([("01","A",0,1),("01","A",0,2)],"02")
    def test_bool_arm(self):
        with self.assertRaises(ValueError): paired_dates([("01","A",True,1)],"02")
    def test_nan(self):
        with self.assertRaises(ValueError): paired_dates([("01","A",0,float("nan"))],"02")
    def test_missing_arm(self):
        rows=[("01","A",0,1),("01","A",1,2),("01","B",0,1),
              ("02","A",0,1),("02","A",1,2)]
        self.assertEqual(paired_dates(rows,"02")["incomplete_arms"],1)
    def test_no_balanced(self):
        rows=[("01","A",0,1),("01","A",1,2),("02","B",0,1),("02","B",1,2)]
        self.assertIsNone(paired_dates(rows,"02")["balanced"])
    def test_no_pair_date(self):
        with self.assertRaises(ValueError):
            paired_dates([("01","A",0,1),("01","A",1,2),("02","A",0,1)],"02")
    def test_missing_period(self):
        with self.assertRaises(ValueError):
            paired_dates([("01","A",0,1),("01","A",1,2)],"02")

if __name__=="__main__": unittest.main()
