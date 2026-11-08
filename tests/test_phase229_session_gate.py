import unittest
from hashlib import sha256
from phase229_session_gate import validate_sessions

def pin(xs):return sha256(('\n'.join(xs)+'\n').encode('ascii')).hexdigest()
class SessionGateTests(unittest.TestCase):
    def setUp(self):
        self.cal=['2025-09-02','2025-09-03','2025-09-04','2025-09-05','2025-09-08']
        self.kw={'source':'illustrative fixture, NOT exchange authenticated','expected_sha256':pin(self.cal)}
    def test_valid_subset(self):
        out=validate_sessions(self.cal[:2],self.cal,**self.kw)
        self.assertFalse(out['calendar_authenticated'])
    def test_labor_day_rejected(self):
        with self.assertRaises(ValueError):validate_sessions(['2025-09-01'],self.cal,**self.kw)
    def test_weekend_rejected(self):
        with self.assertRaises(ValueError):validate_sessions(['2025-09-06'],self.cal,**self.kw)
    def test_tamper_detected(self):
        with self.assertRaises(ValueError):validate_sessions(self.cal[:2],self.cal+['2025-09-09'],**self.kw)
    def test_weekend_calendar_rejected(self):
        cal=['2025-09-05','2025-09-06']
        with self.assertRaises(ValueError):validate_sessions(['2025-09-05'],cal,source='fixture',expected_sha256=pin(cal))
    def test_duplicate_calendar_rejected(self):
        cal=['2025-09-02','2025-09-02']
        with self.assertRaises(ValueError):validate_sessions(['2025-09-02'],cal,source='fixture',expected_sha256=pin(cal))
    def test_missing_source_rejected(self):
        with self.assertRaises(ValueError):validate_sessions(self.cal[:2],self.cal,source='',expected_sha256=pin(self.cal))
    def test_missing_request_rejected(self):
        with self.assertRaises(ValueError):validate_sessions([],self.cal,**self.kw)
if __name__=='__main__':unittest.main()
