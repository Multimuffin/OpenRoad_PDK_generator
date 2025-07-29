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
