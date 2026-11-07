import unittest
from phase205_calendar_provenance import audit_calendar
BASE = {"source_url":"https://example.org/official-schedule","retrieved_utc":"2026-11-07T01:00:00Z","market":"US equities","timezone":"America/New_York","sessions":["2025-11-03","2025-11-04"]}
class TestCalendar(unittest.TestCase):
    def test_complete(self):
        r=audit_calendar(BASE,BASE["sessions"]); self.assertTrue(r["admitted"]); self.assertFalse(r["source_authenticated"])
    def test_missing(self): self.assertEqual(audit_calendar(BASE,["2025-11-03"])["missing_sessions"],["2025-11-04"])
    def test_unexpected(self): self.assertEqual(audit_calendar(BASE,BASE["sessions"]+["2025-11-05"])["unexpected_sessions"],["2025-11-05"])
    def test_duplicate(self): self.assertIn("duplicate_session_date",audit_calendar({**BASE,"sessions":["2025-11-03"]*2},["2025-11-03"])["errors"])
    def test_unordered(self): self.assertIn("unordered_session_date",audit_calendar({**BASE,"sessions":BASE["sessions"][::-1]},BASE["sessions"])["errors"])
    def test_invalid(self): self.assertIn("invalid_session_date",audit_calendar({**BASE,"sessions":["2025-02-30"]},[])["errors"])
    def test_url(self): self.assertIn("invalid_source_url",audit_calendar({**BASE,"source_url":"http://example.org"},BASE["sessions"])["errors"])
    def test_timestamp(self): self.assertIn("invalid_retrieval_timestamp",audit_calendar({**BASE,"retrieved_utc":"yesterday"},BASE["sessions"])["errors"])
    def test_missing_metadata(self): self.assertIn("missing_market",audit_calendar({k:v for k,v in BASE.items() if k!="market"},BASE["sessions"])["errors"])
    def test_determinism(self): self.assertEqual(audit_calendar(BASE,BASE["sessions"])["calendar_document_sha256"],audit_calendar(BASE,BASE["sessions"])["calendar_document_sha256"])
if __name__=="__main__": unittest.main()
