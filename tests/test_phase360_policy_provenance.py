"""Constructed-input checks; not SEC empirical verification."""
import unittest
from copy import deepcopy
from scripts.phase360_policy_provenance import audit_policy_provenance
K=("ABC","2025-10-31")
P={K:["XNAS","XNYS"]}
E={K:dict(source_sha256="a"*64,source_locator="archive://unverified",as_of="2025-10-30",eligible_exchanges=["XNYS","XNAS"])}
class TestPolicyProvenance(unittest.TestCase):
    def test_valid_metadata_not_authenticated(self):
        self.assertFalse(audit_policy_provenance(P,E)["historical_eligibility_authenticated"])
    def test_missing_evidence(self):
        with self.assertRaises(ValueError): audit_policy_provenance(P,{})
    def test_invalid_session(self):
        with self.assertRaises(ValueError): audit_policy_provenance({("ABC","2025-02-30"):["XNAS"]},{("ABC","2025-02-30"):E[K]})
    def test_future_evidence(self):
        e=deepcopy(E);e[K]["as_of"]="2025-11-01"
        with self.assertRaises(ValueError): audit_policy_provenance(P,e)
    def test_policy_disagreement(self):
        e=deepcopy(E);e[K]["eligible_exchanges"]=["XNAS"]
        with self.assertRaises(ValueError): audit_policy_provenance(P,e)
    def test_bad_digest(self):
        e=deepcopy(E);e[K]["source_sha256"]="bad"
        with self.assertRaises(ValueError): audit_policy_provenance(P,e)
    def test_string_exchange_collection(self):
        with self.assertRaises(ValueError): audit_policy_provenance({K:"XNAS"},E)
    def test_duplicate_eligible(self):
        with self.assertRaises(ValueError): audit_policy_provenance({K:["XNAS","XNAS"]},E)
    def test_no_locator(self):
        e=deepcopy(E);e[K]["source_locator"]=""
        with self.assertRaises(ValueError): audit_policy_provenance(P,e)
    def test_order_independence(self):
        self.assertEqual(audit_policy_provenance(P,E)["entries"][K]["eligible_exchanges"],("XNAS","XNYS"))
if __name__=="__main__": unittest.main()
