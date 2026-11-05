"""Complete GitHub tree inventory; synthetic unit tests."""
import unittest
def inventory(response):
    if response.get("truncated") is not False or not isinstance(response.get("tree"),list):
        raise ValueError("complete tree required")
    seen=set(); files=[]
    for e in response["tree"]:
        p=e.get("path")
        if not isinstance(p,str) or p.startswith("/") or "\\" in p or any(s in ("",".","..") for s in p.split("/")) or p in seen:
            raise ValueError("invalid or duplicate path")
        seen.add(p)
        if e.get("type")=="blob":
            if type(e.get("size")) is not int or e["size"]<0: raise ValueError("invalid size")
            files.append(e)
    archives=[e["path"] for e in files if e["path"].lower().endswith((".zip",".7z",".tar",".gz",".parquet",".feather",".pdf"))]
    csvs=[e["path"] for e in files if e["path"].lower().endswith((".csv",".tsv"))]
    return {"files":len(files),"bytes":sum(e["size"] for e in files),"archives":sorted(archives),"tabular":sorted(csvs)}
class Tests(unittest.TestCase):
    def test_empty(self):self.assertEqual(inventory({"truncated":False,"tree":[]})["files"],0)
    def test_types(self):
        r=inventory({"truncated":False,"tree":[{"path":"x.zip","type":"blob","size":3},{"path":"x.csv","type":"blob","size":2}]})
        self.assertEqual((r["bytes"],r["archives"],r["tabular"]),(5,["x.zip"],["x.csv"]))
    def test_truncated(self):
        with self.assertRaises(ValueError):inventory({"truncated":True,"tree":[]})
    def test_missing_tree(self):
        with self.assertRaises(ValueError):inventory({"truncated":False})
    def test_duplicate(self):
        with self.assertRaises(ValueError):inventory({"truncated":False,"tree":[{"path":"a","type":"tree"},{"path":"a","type":"tree"}]})
    def test_traversal(self):
        for p in ("../a","a/../b","/a","a//b","a\\b"):
            with self.subTest(path=p),self.assertRaises(ValueError):inventory({"truncated":False,"tree":[{"path":p,"type":"tree"}]})
    def test_size(self):
        with self.assertRaises(ValueError):inventory({"truncated":False,"tree":[{"path":"a","type":"blob","size":-1}]})
if __name__=="__main__":unittest.main()
