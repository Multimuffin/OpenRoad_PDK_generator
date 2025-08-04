from pathlib import Path
import re

def find_macros_in_lef(lef_path: Path, macro_prefix: str) -> str:
    """
    Sucht im LEF-File nach Zeilen, die mit 'MACRO <macro_prefix>' beginnen,
    und gibt alle gefundenen Namen als Leerzeichen-getrennten String zurück.
    """
    pattern = re.compile(rf"^MACRO\s+({macro_prefix}\S+)")
    found = []
    with lef_path.open("r") as f:
        for line in f:
            match = pattern.match(line.strip())
            if match:
                found.append(match.group(1))
    return " ".join(found)
