import unittest
from phase440_identity_audit import audit

def r(s='ABC',e='X',g='G',a='1'):
    return dict(security=s,exchange=e,match_group=g,treated=a)

class IdentityTests(unittest.TestCase):
    def test_cross_exchange_not_unstable(self):
        x=audit([r(e='X'),r(e='Y')]);self.assertEqual(x['unstable_security_exchange_assignments'],[]);self.assertEqual(x['securities_on_multiple_exchanges'],['ABC'])
    def test_within_exchange_arm_change(self):
        self.assertEqual(audit([r(),r(a='0')])['unstable_security_exchange_assignments'],['ABC@X'])
    def test_within_exchange_group_change(self):
        self.assertEqual(audit([r(),r(g='H')])['unstable_security_exchange_assignments'],['ABC@X'])
    def test_empty(self):
        with self.assertRaises(ValueError):audit([])
    def test_invalid(self):
        with self.assertRaises(ValueError):audit([r(a='2')])
    def test_no_estimate(self):
        self.assertFalse(audit([r()])['historical_effect_estimated'])
if __name__=='__main__':unittest.main()
