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
    ui_title: str = None
):
    """
    Find files, optionally ask user, create symlink, and update config export.
    """
    dst_dir.mkdir(parents=True, exist_ok=True)
    files = list(src_dir.glob(pattern))
    if not files:
        print(f"Keine Dateien für {export_key} gefunden!")
        return
    if ask_user and len(files) > 1:
        from pdk_gen.ui_utils import list_dir
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
    Liefert den Zellnamen mit oder ohne _WB, je nach Platform-Name.
    Zusätzliche Argumente werden angehängt (z.B. Ports).
    """
    wb = "_WB" if "_wb" in platform_name else ""
    cell = f"{base}{wb}{suffix}"
    if args:
        cell += " " + " ".join(args)
    return cell
