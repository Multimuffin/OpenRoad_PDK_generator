import unittest
from pathlib import Path
from pdk_gen.symlink_utils import create_symlink
import tempfile

class TestSymlinkUtils(unittest.TestCase):
    def test_create_symlink(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            print(f"Temporary directory created at: {tmp_path}")
            src = tmp_path / "orig.txt"
            src.write_text("hello")
            dst = tmp_path / "link.txt"

            create_symlink(src, dst)
            self.assertTrue(dst.is_symlink())
            self.assertEqual(dst.read_text(), "hello")

            src2 = tmp_path / "orig2.txt"
            src2.write_text("world")
            create_symlink(src2, dst, overwrite=True)
            self.assertEqual(dst.read_text(), "world")

if __name__ == "__main__":
    unittest.main()
