"""Deterministic tests using constructed observations, not SEC data."""
import unittest
from scripts.phase459_placebo_grid import placebo_grid

def fixture():
    out=[]
    for day,gap in [("2025-09-01",1),("2025-09-02",1),("2025-09-03",2),
                    ("2025-09-04",2),("2025-10-01",5),("2025-10-02",5)]:
        out.extend([dict(security="T",exchange="X",matched_group="G",date=day,treated=True,outcome=gap),
                    dict(security="C",exchange="X",matched_group="G",date=day,treated=False,outcome=0)])
    return out

class TestPlaceboGrid(unittest.TestCase):
    def test_grid(self):
        result=placebo_grid(fixture(),["2025-09-03","2025-10-01"])
        self.assertEqual([r["eligible_groups"] for r in result["placebos"]],[1,1])
        self.assertAlmostEqual(result["placebos"][1]["equal_group_effect"],3.5)
        self.assertEqual(result["placebos"][0]["fixed_support_groups"],1)
    def test_duplicate(self):
        rows=fixture(); rows.append(rows[0])
        self.assertRaises(ValueError,placebo_grid,rows,["2025-10-01"])
    def test_assignment_drift(self):
        rows=fixture(); rows[-2]["matched_group"]="OTHER"
        self.assertRaises(ValueError,placebo_grid,rows,["2025-10-01"])
    def test_cross_exchange(self):
        rows=fixture(); rows.append(dict(security="T",exchange="Y",matched_group="G",date="2025-10-02",treated=False,outcome=1))
        self.assertRaises(ValueError,placebo_grid,rows,["2025-10-01"])
    def test_no_support(self):
        result=placebo_grid(fixture(),["2025-10-02"])
        self.assertIsNone(result["placebos"][0]["equal_group_effect"])
    def test_duplicate_boundaries(self):
        self.assertRaises(ValueError,placebo_grid,fixture(),["2025-10-01","2025-10-01"])
    def test_boolean_outcome(self):
        rows=fixture(); rows[0]["outcome"]=True
        self.assertRaises(ValueError,placebo_grid,rows,["2025-10-01"])
    def test_unpaired_count(self):
        rows=fixture(); rows.append(dict(security="Z",exchange="Y",matched_group="G",date="2025-10-02",treated=True,outcome=1))
        self.assertEqual(placebo_grid(rows,["2025-10-01"])["unpaired_cells"],1)

if __name__=="__main__":
    unittest.main()
