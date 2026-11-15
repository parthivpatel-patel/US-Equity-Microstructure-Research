import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from phase392_archive_inventory import inspect_archive


class InventoryTests(unittest.TestCase):
    def make(self, entries):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        path = Path(temp.name) / 'fixture.zip'
        with zipfile.ZipFile(path, 'w') as z:
            for name, data in entries:
                z.writestr(name, data)
        return path

    def test_regular(self):
        result = inspect_archive(self.make([('paper.txt', 'research')]))
        self.assertEqual(result['issues'], [])
        self.assertEqual(result['member_count'], 1)
        self.assertFalse(result['contents_authenticated'])
        self.assertFalse(result['safe_to_extract'])

    def test_traversal(self):
        self.assertTrue(any(x.startswith('unsafe_path:') for x in inspect_archive(self.make([('../escape', 'x')]))['issues']))

    def test_absolute(self):
        self.assertTrue(any(x.startswith('unsafe_path:') for x in inspect_archive(self.make([('/etc/passwd', 'x')]))['issues']))

    def test_backslash(self):
        self.assertTrue(any(x.startswith('unsafe_path:') for x in inspect_archive(self.make([('..\\escape', 'x')]))['issues']))

    def test_duplicate(self):
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            result = inspect_archive(self.make([('same', 'a'), ('same', 'b')]))
        self.assertIn('duplicate_member:same', result['issues'])

    def test_total_limit(self):
        self.assertIn('uncompressed_limit_exceeded', inspect_archive(self.make([('a', '1234')]), max_uncompressed=3)['issues'])

    def test_member_limit(self):
        self.assertIn('member_limit_exceeded', inspect_archive(self.make([('a', '1'), ('b', '2')]), max_members=1)['issues'])

    def test_sha_stable(self):
        p = self.make([('a', '1')])
        self.assertEqual(inspect_archive(p)['archive_sha256'], inspect_archive(p)['archive_sha256'])


if __name__ == '__main__':
    unittest.main()
