"""Deterministic malformed-input regressions; no SEC data or source authentication."""
import unittest
from scripts.phase360_policy_provenance import audit_policy_provenance
K=('ABC','2025-10-31')
E={K:dict(source_sha256='a'*64,source_locator='fixture://not-real',as_of='2025-10-30',eligible_exchanges=['XNAS'])}
class TestMalformedExchange(unittest.TestCase):
    def test_noniterable_policy(self):
        for bad in (None, 12, 2.5):
            with self.subTest(bad=bad), self.assertRaises(ValueError): audit_policy_provenance({K:bad},E)
    def test_nested_policy(self):
        with self.assertRaises(ValueError): audit_policy_provenance({K:[['XNAS']]},E)
    def test_nested_evidence(self):
        e={K:{**E[K], 'eligible_exchanges':[['XNAS']]}}
        with self.assertRaises(ValueError): audit_policy_provenance({K:['XNAS']},e)
    def test_nonstring_evidence(self):
        e={K:{**E[K], 'eligible_exchanges':[123]}}
        with self.assertRaises(ValueError): audit_policy_provenance({K:['XNAS']},e)
    def test_valid_fixture_still_unauthenticated(self):
        result=audit_policy_provenance({K:['XNAS']},E)
        self.assertFalse(result['source_bytes_authenticated'])
        self.assertFalse(result['historical_eligibility_authenticated'])
if __name__=='__main__': unittest.main()
