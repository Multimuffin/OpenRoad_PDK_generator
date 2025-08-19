from pathlib import Path
from pdk_gen.symlink_utils import create_symlink
from pdk_gen.ui_utils import list_dir

def handle_resource(
    src_dir: Path,
    dst_dir: Path,
    pattern: str,
    export_key: str,
    updater,
    ask_user: bool = False,
    ui_title: str = None
):
    """
    Find files, optionally ask user, create symlink, and update config export.
    """
    dst_dir.mkdir(parents=True, exist_ok=True)
    files = list(src_dir.glob(pattern))
    if not files:
        print(f"No files found for {export_key}!")
        return
    if ask_user and len(files) > 1:
        names = [f.name for f in files]
        selected_name = list_dir(names, title=ui_title or export_key, width=1)
        file = next(f for f in files if f.name == selected_name)
    else:
        file = files[0]
    dst = dst_dir / file.name
    create_symlink(file, dst)
    updater._update_export(export_key, [dst])

def cell_name_with_wb(platform_name: str, base: str, suffix: str = "", *args: str) -> str:
    """
    Returns the cell name with or without _WB, depending on the platform name.
    Additional arguments are appended (e.g. ports).
    """
    wb = "_WB" if "_wb" in platform_name else ""
    cell = f"{base}{wb}{suffix}"
    if args:
        cell += " " + " ".join(args)
    return cell
