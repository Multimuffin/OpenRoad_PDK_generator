# tests/test_file_finder.py
import unittest
from pathlib import Path
from pdk_generator.file_finder import natural_key, find_all, find_first, list_subdirs

class TestFileFinder(unittest.TestCase):
    def test_natural_key_sorting(self):
        names = ["file10.txt", "file2.txt", "file1.txt"]
        sorted_names = sorted(names, key=natural_key)
        self.assertEqual(sorted_names, ["file1.txt", "file2.txt", "file10.txt"])

    def test_find_all_and_first(self):
        import tempfile
        tmp = Path(tempfile.mkdtemp())
        (tmp/"a.lef").write_text("")
        (tmp/"b.lef").write_text("")
        (tmp/"c.txt").write_text("")
        all_lef = find_all(tmp, "*.lef")
        self.assertEqual(len(all_lef), 2)
        first = find_first(tmp, "*.lef")
        self.assertIn(first.name, {"a.lef","b.lef"})

    def test_list_subdirs(self):
        import tempfile
        tmp = Path(tempfile.mkdtemp())
        (tmp/"sub1").mkdir()
        (tmp/"sub2").mkdir()
        subdirs = list_subdirs(tmp)
        self.assertSetEqual({d.name for d in subdirs}, {"sub1","sub2"})

if __name__=="__main__":
    unittest.main()
