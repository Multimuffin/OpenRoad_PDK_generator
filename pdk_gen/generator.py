import json
import shutil
import subprocess
from pathlib import Path
import logging
from .setup_config import load_user_config

from .file_finder import list_subdirs
from .symlink_utils import batch_symlink
from .config_updater import ConfigUpdater

logger = logging.getLogger(__name__)

def generate_platform(tech_name: str, m_stack: str, metal_subdir=None) -> None:
    """
    High-level orchestration of the PDK platform generation workflow.
    Now also takes m_stack (Metal Stack) as argument.
    Steps:
      1. Determine directories
      2. Create platform folders
      3. Copy template and write args JSON
      4. Invoke ConfigUpdater
      5. Create necessary symlinks
    """
    # 1) Determine project structure
    config = load_user_config()
    project_root = Path.cwd()
    scripts_dir  = project_root / "scripts"
    platforms_dir = Path(config["platforms_root"])
    target_dir   = platforms_dir / f"{tech_name}_{m_stack}"

    template_cfg = project_root / "src" / "config.mk"
    target_cfg   = target_dir / "config.mk"
    args_json    = target_dir / "modify_args.json"

    # 2) Create (or empty) target directory
    if target_dir.exists():
        logger.info(f"Overwriting existing platform directory: {target_dir}")
    else:
        logger.info(f"Creating platform directory: {target_dir}")
    target_dir.mkdir(parents=True, exist_ok=True)

    # 3) Copy template and write JSON
    logger.info(f"Copying template config.mk to {target_cfg}")
    shutil.copy2(template_cfg, target_cfg)

    payload = {
        "platform_name": tech_name,
        "m_stack": m_stack,
        "generation_script_directory": str(scripts_dir),
        "project_root": str(project_root),
        "platforms_dir": str(platforms_dir),
        "new_platform": str(target_dir),
        "config_template": str(template_cfg),
        "config_file": str(target_cfg),
    }
    logger.debug(f"Writing modify_args.json: {payload}")
    with args_json.open("w") as f:
        json.dump(payload, f, indent=2)

    # 4) Update config.mk via ConfigUpdater
    updater = ConfigUpdater(cfg_path=target_cfg, args_path=args_json)
    updater.load()
    updater.apply_all(metal_subdir=metal_subdir)   # handles TECH_DIR, TECH_LEF, etc.
    updater.write()

    # 5) Create symlinks for all required resources
    #    Assume updater.symlink_pairs is a list of (src_path, dst_path)
    symlink_pairs = updater.symlink_pairs
    batch_symlink(symlink_pairs)

    logger.info("Platform generation finished successfully.")
