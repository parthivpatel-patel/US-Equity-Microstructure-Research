import unittest
from phase234_calendar_evidence_validator import validate_calendar_evidence
BASE = dict(source_url="https://www.nyse.com/markets/hours-calendars", retrieved_at="2026-11-08T06:00:00Z", raw_sha256="a"*64)
class CalendarEvidenceTests(unittest.TestCase):
    def check_reject(self, dates, **changes):
        with self.assertRaises(ValueError):
            validate_calendar_evidence(dates, **(BASE | changes))
    def test_valid_structure_does_not_authenticate(self):
        r = validate_calendar_evidence(["2025-09-02", "2025-09-03"], **BASE)
        self.assertFalse(r["historical_calendar_authenticated"])
        self.assertEqual(r["retrieved_at"], "2026-11-08T06:00:00+00:00")
    def test_weekend(self): self.check_reject(["2025-09-06"])
    def test_duplicates(self): self.check_reject(["2025-09-02"]*2)
    def test_unsorted(self): self.check_reject(["2025-09-03", "2025-09-02"])
    def test_noncanonical(self): self.check_reject(["2025-9-2"])
    def test_http(self): self.check_reject(["2025-09-02"], source_url="http://example.com")
    def test_credentials(self): self.check_reject(["2025-09-02"], source_url="https://secret@example.com/x")
    def test_naive_timestamp(self): self.check_reject(["2025-09-02"], retrieved_at="2026-11-08T06:00:00")
    def test_bad_digest(self): self.check_reject(["2025-09-02"], raw_sha256="z"*64)
    def test_holiday_not_authenticated(self):
        r = validate_calendar_evidence(["2025-09-01"], **BASE)
        self.assertFalse(r["historical_calendar_authenticated"])
if __name__ == "__main__": unittest.main()
