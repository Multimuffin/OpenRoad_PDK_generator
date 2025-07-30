from pathlib import Path
import sys
import os
import re

def list_dir(src_dir, title="Available Options", width=4):
    """
    Show a formatted list of subdirectories and let the user select one.
    Returns the selected directory name.
    """
    subdir = [d for d in os.listdir(src_dir) if (Path(src_dir) / d).is_dir()]
    if not subdir:
        print(f"No folders found under {src_dir}")
        sys.exit(1)
    subdir.sort()
    entries = [f"{i}) {name}" for i, name in enumerate(subdir, 1)]
    cols = width
    total = len(entries)
    rows = total // cols + (1 if total % cols else 0)
    col_width = max(len(e) for e in entries) + 2
    table_width = cols * col_width
    print()
    print(title.center(table_width))
    print("-" * table_width)
    for r in range(rows):
        row = []
        for c in range(cols):
            idx = c * rows + r
            if idx < total:
                row.append(entries[idx].ljust(col_width))
        print("".join(row))
    print("-" * table_width)
    attempts = 0
    while attempts < 3:
        sel = input(f"Select the ID to use [1-{total}]: ")
        if sel.isdigit():
            sel_idx = int(sel)
            if 1 <= sel_idx <= total:
                lib_val = subdir[sel_idx - 1]
                print(f"\nSelected: {lib_val}")
                return lib_val
            else:
                print("Selection out of range.")
        else:
            print("Invalid input; please enter a number.")
        attempts += 1
        if attempts < 3:
            print("Please try again.\n")
    print("Too many invalid attempts...\n   --> aborting!")
    sys.exit(1)
