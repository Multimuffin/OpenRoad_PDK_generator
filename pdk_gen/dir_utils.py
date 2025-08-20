from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def create_platform_dirs(base_dir: Path) -> None:
    """
    Create all required subdirectories for a new platform.
    """
    for sub in ["gds", "cdl", "lef", "lib"]:
        dir_path = base_dir / sub
        dir_path.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Created directory: {dir_path}")

def create_named_dir(base_dir: Path, name: str) -> Path:
    """
    Create a subdirectory with the given name under base_dir and return its Path.
    """
    dir_path = base_dir / name
    dir_path.mkdir(parents=True, exist_ok=True)
    logger.debug(f"Created directory: {dir_path}")
    return dir_path
