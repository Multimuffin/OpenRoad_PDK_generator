from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def create_symlink(src: Path, dst: Path, overwrite: bool = True) -> None:
    """
    Create a symbolic link at `dst` pointing to `src`.
    If `overwrite` is True and `dst` already exists (file or symlink), it will be removed first.
    """
    src = Path(src)
    dst = Path(dst)

    # Ensure parent directory exists
    dst.parent.mkdir(parents=True, exist_ok=True)

    if overwrite and dst.exists() or dst.is_symlink():
        dst.unlink()
        logger.debug(f"Removed existing path at {dst}")

    dst.symlink_to(src)
    logger.info(f"Created symlink: {dst} -> {src}")

def batch_symlink(pairs: list[tuple[Path, Path]], overwrite: bool = True) -> None:
    """
    Create multiple symlinks.
    :param pairs: List of tuples (src, dst).
    :param overwrite: Passed through to create_symlink.
    """
    for src, dst in pairs:
        try:
            create_symlink(src, dst, overwrite=overwrite)
        except Exception as e:
            logger.error(f"Failed to link {dst} -> {src}: {e}")

def handle_resource(
    src_dir: Path,
    dst_dir: Path,
    pattern: str,
    export_key: str,
    updater,
    ask_user: bool = False,
    ui_title: str = None,
    return_only: bool = False
):
    """
    Find files, optionally ask user, create symlink, and update config export or return symlink paths.
    """
    dst_dir.mkdir(parents=True, exist_ok=True)
    files = list(src_dir.glob(pattern))
    if not files:
        print(f"No files found for {export_key}!")
        return [] if return_only else None
    symlink_paths = []
    if ask_user and len(files) > 1:
        from pdk_gen.ui_utils import list_dir
        names = [f.name for f in files]
        selected_name = list_dir(names, title=ui_title or export_key, width=1)
        file = next(f for f in files if f.name == selected_name)
        dst = dst_dir / file.name
        create_symlink(file, dst)
        symlink_paths.append(dst)
    else:
        for file in files:
            dst = dst_dir / file.name
            create_symlink(file, dst)
            symlink_paths.append(dst)
    if return_only:
        return symlink_paths
    else:
        updater._update_export(export_key, symlink_paths)

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
