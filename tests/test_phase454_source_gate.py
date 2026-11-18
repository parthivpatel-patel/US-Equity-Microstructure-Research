"""Constructed fixtures only: no historical observations."""
import hashlib
import unittest
from scripts.phase454_source_gate import verify_inputs

OBS=b"security,exchange,matched_group,date,treated,outcome\nAAA,X,G,2025-10-01,True,1.5\nBBB,X,G,2025-10-01,False,0.5\n"
CAL=b"date\n2025-10-01\n2025-10-02\n"
def manifest(a=OBS,b=CAL):
    return {"observations_sha256":hashlib.sha256(a).hexdigest(),"calendar_sha256":hashlib.sha256(b).hexdigest()}
class TestSourceGate(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(verify_inputs(OBS,CAL,manifest())["observation_rows"],2)
    def test_tamper(self):
        with self.assertRaisesRegex(ValueError,"digest mismatch"):verify_inputs(OBS+b" ",CAL,manifest())
    def test_missing_digest(self):
        with self.assertRaisesRegex(ValueError,"invalid expected digest"):verify_inputs(OBS,CAL,{})
    def test_outside_calendar(self):
        a=OBS.replace(b"2025-10-01",b"2025-10-03")
        with self.assertRaisesRegex(ValueError,"outside"):verify_inputs(a,CAL,manifest(a,CAL))
    def test_duplicate(self):
        a=OBS+OBS.split(b"\n")[1]+b"\n"
        with self.assertRaisesRegex(ValueError,"duplicate security"):verify_inputs(a,CAL,manifest(a,CAL))
    def test_bad_treatment(self):
        a=OBS.replace(b"True",b"1")
        with self.assertRaisesRegex(ValueError,"treatment"):verify_inputs(a,CAL,manifest(a,CAL))
    def test_nonfinite(self):
        a=OBS.replace(b"1.5",b"nan")
        with self.assertRaisesRegex(ValueError,"nonfinite"):verify_inputs(a,CAL,manifest(a,CAL))
    def test_duplicate_calendar(self):
        b=CAL+b"2025-10-02\n"
        with self.assertRaisesRegex(ValueError,"duplicate calendar"):verify_inputs(OBS,b,manifest(OBS,b))
if __name__=="__main__": unittest.main()
