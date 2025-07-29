from pathlib import Path
import pytest
from pdk_generator.symlink_utils import create_symlink

def test_create_symlink(tmp_path):
    src = tmp_path / "orig.txt"
    src.write_text("hello")
    dst = tmp_path / "link.txt"

    create_symlink(src, dst)
    assert dst.is_symlink()
    assert dst.read_text() == "hello"
    
    # overwrite existing dst
    src2 = tmp_path / "orig2.txt"
    src2.write_text("world")
    create_symlink(src2, dst, overwrite=True)
    assert dst.read_text() == "world"
