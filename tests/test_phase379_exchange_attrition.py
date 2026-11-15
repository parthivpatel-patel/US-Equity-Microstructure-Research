import unittest
from fractions import Fraction
from scripts.phase379_exchange_attrition import audit_attrition

class TestAudit(unittest.TestCase):
    def setUp(self):
        self.rows=[(p,d,e,a,1,2) for p in ('p1','p2') for d in ('pre','post') for e in ('X','Y') for a in ('T','C')]
    def test_complete(self):
        r=audit_attrition(self.rows,['pre'],['post'])
        self.assertEqual(r['expected_rows'],16)
        self.assertEqual(r['missing_keys'],())
        self.assertEqual(r['by_exchange']['X']['retention'],Fraction(1))
    def test_missing_one(self):
        rows=[r for r in self.rows if r[:4]!=('p2','post','Y','C')]
        result=audit_attrition(rows,['pre'],['post'])
        self.assertEqual(result['by_exchange']['Y']['retention'],Fraction(1,2))
        self.assertEqual(result['by_exchange']['X']['retention'],Fraction(1))
        self.assertEqual(result['missing_keys'],(('p2','post','Y','C'),))
    def test_duplicate(self):
        with self.assertRaisesRegex(ValueError,'duplicate'):audit_attrition(self.rows+[self.rows[0]],['pre'],['post'])
    def test_invalid_counts(self):
        with self.assertRaisesRegex(ValueError,'counts'):audit_attrition([('p','pre','X','T',3,2)],['pre'],['post'])
    def test_overlap(self):
        with self.assertRaisesRegex(ValueError,'windows'):audit_attrition(self.rows,['pre'],['pre'])
    def test_empty(self):
        with self.assertRaisesRegex(ValueError,'empty'):audit_attrition([],['pre'],['post'])
    def test_extra_date(self):
        with self.assertRaisesRegex(ValueError,'keys'):audit_attrition([('p','other','X','T',1,2)],['pre'],['post'])

if __name__=='__main__':unittest.main()
