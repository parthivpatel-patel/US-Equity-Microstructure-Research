import unittest
from phase233_calendar_evidence import assess_calendar_evidence

BASE = dict(source_url='https://example.org/source', retrieved_at='2026-11-08T05:00:00Z', raw_sha256='a'*64)

class CalendarEvidenceTests(unittest.TestCase):
    def test_digest_deterministic(self):
        a = assess_calendar_evidence(['2025-09-02'], **BASE)
        b = assess_calendar_evidence(['2025-09-02'], **BASE)
        self.assertEqual(a['roster_sha256'], b['roster_sha256'])
        self.assertFalse(a['historical_calendar_authenticated'])
    def test_attestation_not_enough(self):
        x = assess_calendar_evidence(['2025-09-02'], independently_checked=True, reviewer_evidence='audit note', **BASE)
        self.assertFalse(x['historical_calendar_authenticated'])
        self.assertTrue(x['independent_check_documented'])
    def test_missing_evidence_rejected(self):
        with self.assertRaises(ValueError):
            assess_calendar_evidence(['2025-09-02'], independently_checked=True, **BASE)
    def test_bad_hash_rejected(self):
        with self.assertRaises(ValueError):
            assess_calendar_evidence(['2025-09-02'], **{**BASE, 'raw_sha256':'z'*64})
    def test_missing_source_rejected(self):
        with self.assertRaises(ValueError):
            assess_calendar_evidence(['2025-09-02'], **{**BASE, 'source_url':''})
    def test_empty_roster_rejected(self):
        with self.assertRaises(ValueError):
            assess_calendar_evidence([], **BASE)
    def test_nonboolean_check_rejected(self):
        with self.assertRaises(ValueError):
            assess_calendar_evidence(['2025-09-02'], independently_checked='yes', **BASE)

if __name__ == '__main__': unittest.main()
