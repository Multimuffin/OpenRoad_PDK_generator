from pathlib import Path
import re
from typing import List, Optional

def natural_key(s: str):
    """
    Split a string into numeric and non-numeric parts for natural sorting.
    E.g. "file2.txt" comes before "file10.txt".
    """
    parts = re.split(r'(\d+)', s)
    return [int(p) if p.isdigit() else p.lower() for p in parts]

def find_all(directory: Path, pattern: str) -> List[Path]:
    """
    Return all files in `directory` matching the glob `pattern`,
    sorted using natural order on filenames.
    """
    return sorted(directory.glob(pattern), key=lambda p: natural_key(p.name))

def find_first(directory: Path, pattern: str) -> Optional[Path]:
    """
    Return the first file matching the glob `pattern` in `directory`,
    or None if there are no matches.
    """
    matches = find_all(directory, pattern)  
    return matches[0] if matches else None

def list_subdirs(directory: Path, reverse: bool = False) -> List[Path]:
    """
    Return all subdirectories of `directory`, naturally sorted.
    Set `reverse=True` to sort in descending order.
    """
    dirs = [p for p in directory.iterdir() if p.is_dir()]
    return sorted(dirs, key=lambda p: natural_key(p.name), reverse=reverse)

def find_lib_files_by_corner(lib_dir: Path, corner: str):
    """
    Returns all LIB files in the directory that match the corner (ff, tt, ss).
    """
    pattern = f"*_{corner}_*.lib"
    return list(lib_dir.glob(pattern))
