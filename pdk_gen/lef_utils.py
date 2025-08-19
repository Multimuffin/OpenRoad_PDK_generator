from pathlib import Path
import re

def find_macros_in_lef(lef_path: Path, macro_prefix: str) -> str:
    """
    Searches the LEF file for lines beginning with ‘MACRO <macro_prefix>’
    and returns all names found as a space-separated string.
    """
    pattern = re.compile(rf"^MACRO\s+({macro_prefix}\S+)")
    found = []
    with lef_path.open("r") as f:
        for line in f:
            match = pattern.match(line.strip())
            if match:
                found.append(match.group(1))
    return " ".join(found)
