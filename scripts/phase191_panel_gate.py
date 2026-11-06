"""Fail-closed structural and provenance gate. Flags are declarations, not independent authentication."""
import csv,hashlib,json,math,sys
from datetime import date
from pathlib import Path
FIELDS=('security_id','exchange','trade_date','matched_group_id','outcome','contrast_pp')
def audit(csv_path,manifest_path):
    path=Path(csv_path); m=json.loads(Path(manifest_path).read_text())
    if set(m)!={'sha256','source_url','retrieved_utc','license_reviewed','treatment_authenticated'}: raise ValueError('manifest schema mismatch')
    if not isinstance(m['source_url'],str) or not m['source_url'].startswith('https://'): raise ValueError('missing source URL')
    if m['license_reviewed'] is not True or m['treatment_authenticated'] is not True: raise ValueError('provenance or treatment authentication incomplete')
    digest=hashlib.sha256(path.read_bytes()).hexdigest()
    if digest!=m['sha256']: raise ValueError('source checksum mismatch')
    if not isinstance(m['retrieved_utc'],str) or not m['retrieved_utc'].endswith('Z'): raise ValueError('missing UTC retrieval timestamp')
    keys=set();dates=set();groups=set();outcomes=set();n=0
    with path.open(newline='',encoding='utf-8') as f:
        reader=csv.DictReader(f)
        if tuple(reader.fieldnames or ())!=FIELDS: raise ValueError('CSV schema mismatch')
        for row in reader:
            if any(not row[k] or row[k].strip()!=row[k] for k in FIELDS): raise ValueError('missing or untrimmed field')
            if row['outcome'] not in {'count','volume'}: raise ValueError('invalid outcome')
            try:
                d=date.fromisoformat(row['trade_date'])
                if d.isoformat()!=row['trade_date'] or d.weekday()>=5: raise ValueError()
                if not math.isfinite(float(row['contrast_pp'])): raise ValueError()
            except ValueError: raise ValueError('invalid date or contrast')
            key=tuple(row[k] for k in FIELDS[:-1])
            if key in keys: raise ValueError('duplicate security/exchange/date/group/outcome')
            keys.add(key);dates.add(row['trade_date']);groups.add(row['matched_group_id']);outcomes.add(row['outcome']);n+=1
    if not n: raise ValueError('empty panel')
    return {'rows':n,'dates':len(dates),'groups':len(groups),'outcomes':sorted(outcomes),'sha256':digest,'status':'structural gate passed; independent authentication still required'}
if __name__=='__main__':
    if len(sys.argv)!=3: raise SystemExit('usage: python scripts/phase191_panel_gate.py panel.csv manifest.json')
    print(json.dumps(audit(sys.argv[1],sys.argv[2]),indent=2))
