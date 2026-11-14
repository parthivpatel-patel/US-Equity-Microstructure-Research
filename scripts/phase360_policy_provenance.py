"""Metadata-only evidence gate. Does not authenticate historical source bytes."""
from datetime import date
import re
def audit_policy_provenance(policy,evidence):
    if not isinstance(policy,dict) or not policy or not isinstance(evidence,dict) or set(policy)!=set(evidence):
        raise ValueError("missing or mismatched policy/evidence")
    result={}
    for key,exchanges in policy.items():
        if not isinstance(key,tuple) or len(key)!=2 or not all(isinstance(v,str) and v.strip() for v in key):
            raise ValueError("invalid key")
        try: session=date.fromisoformat(key[1])
        except ValueError as exc: raise ValueError("invalid session") from exc
        if session.isoformat()!=key[1] or isinstance(exchanges,(str,bytes)):
            raise ValueError("invalid session or exchange collection")
        exchanges=tuple(exchanges)
        if not exchanges or len(set(exchanges))!=len(exchanges) or any(not isinstance(v,str) or not v.strip() for v in exchanges):
            raise ValueError("invalid exchanges")
        item=evidence[key]
        if not isinstance(item,dict) or set(item)!={"source_sha256","source_locator","as_of","eligible_exchanges"}:
            raise ValueError("invalid evidence schema")
        digest=item["source_sha256"]
        if not isinstance(digest,str) or re.fullmatch(r"[0-9a-f]{64}",digest) is None:
            raise ValueError("invalid digest")
        locator=item["source_locator"]
        if not isinstance(locator,str) or not locator.strip(): raise ValueError("missing locator")
        try: as_of=date.fromisoformat(item["as_of"])
        except (ValueError,TypeError) as exc: raise ValueError("invalid as-of date") from exc
        if as_of.isoformat()!=item["as_of"] or as_of>session: raise ValueError("invalid as-of chronology")
        documented=item["eligible_exchanges"]
        if isinstance(documented,(str,bytes)) or not isinstance(documented,(list,tuple,set)) or len(documented)!=len(set(documented)) or set(documented)!=set(exchanges):
            raise ValueError("policy/evidence contradiction")
        result[key]={"source_sha256":digest,"source_locator":locator,"as_of":item["as_of"],"eligible_exchanges":tuple(sorted(exchanges))}
    return {"entries":result,"source_bytes_authenticated":False,"historical_eligibility_authenticated":False,"status":"METADATA_ONLY_NOT_EMPIRICAL_AUTHENTICATION"}
