import unittest
from datetime import datetime, timezone
from scripts.phase419_source_policy import check_manifest_policy

NOW = datetime(2026, 11, 16, 23, 0, tzinfo=timezone.utc)
BASE = {'sources': [{'retrieved_utc': '2026-11-16T22:59:00Z', 'source_url': 'https://www.sec.gov/data.csv'}]}

class PolicyTests(unittest.TestCase):
    def check(self, **updates):
        return check_manifest_policy({'sources': [{**BASE['sources'][0], **updates}]}, NOW)
    def test_normal_pass_no_authentication(self):
        r = self.check()
        self.assertEqual(r['status'], 'POLICY_PASS_NOT_AUTHENTICATED')
        self.assertFalse(r['source_authenticated'])
    def test_future_rejected(self):
        self.assertEqual(self.check(retrieved_utc='2099-01-01T00:00:00Z')['status'], 'BLOCKED')
    def test_tolerance_boundary(self):
        self.assertEqual(self.check(retrieved_utc='2026-11-16T23:05:00Z')['status'], 'POLICY_PASS_NOT_AUTHENTICATED')
    def test_over_tolerance(self):
        self.assertEqual(self.check(retrieved_utc='2026-11-16T23:05:01Z')['status'], 'BLOCKED')
    def test_localhost(self):
        self.assertEqual(self.check(source_url='https://localhost/data')['status'], 'BLOCKED')
    def test_loopback_ipv4(self):
        self.assertEqual(self.check(source_url='https://127.0.0.1/data')['status'], 'BLOCKED')
    def test_private_ipv4(self):
        self.assertEqual(self.check(source_url='https://10.1.1.1/data')['status'], 'BLOCKED')
    def test_loopback_ipv6(self):
        self.assertEqual(self.check(source_url='https://[::1]/data')['status'], 'BLOCKED')
    def test_userinfo(self):
        self.assertEqual(self.check(source_url='https://www.sec.gov@evil.example/data')['status'], 'BLOCKED')
    def test_non_authoritative_public_domain_not_authenticated(self):
        self.assertEqual(self.check(source_url='https://example.com/fake.csv')['status'], 'POLICY_PASS_NOT_AUTHENTICATED')
    def test_naive_asof(self):
        with self.assertRaises(ValueError): check_manifest_policy(BASE, datetime(2026, 11, 16))
    def test_negative_tolerance(self):
        with self.assertRaises(ValueError): check_manifest_policy(BASE, NOW, -1)
    def test_empty(self):
        self.assertEqual(check_manifest_policy({'sources': []}, NOW)['status'], 'BLOCKED')
    def test_bad_timestamp(self):
        self.assertEqual(self.check(retrieved_utc='yesterday')['status'], 'BLOCKED')
    def test_invalid_hostname(self):
        self.assertEqual(self.check(source_url='https://bad..example/path')['status'], 'BLOCKED')

if __name__ == '__main__': unittest.main()
