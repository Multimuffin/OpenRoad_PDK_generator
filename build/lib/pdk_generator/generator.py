import json
import shutil
import subprocess
from pathlib import Path
import logging

from pdk_generator.file_finder import list_subdirs
from pdk_generator.symlink_utils import batch_symlink
from pdk_generator.config_updater import ConfigUpdater

logger = logging.getLogger(__name__)

def generate_platform(tech_name: str, m_stack: str) -> None:
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
    # project_root = Path(__file__).resolve().parent.parent  # original
    project_root = Path.cwd()  # <--- changed for robust path handling
    scripts_dir  = project_root / "scripts"
    platforms_dir = project_root / "platforms"
    target_dir   = platforms_dir / tech_name

    template_cfg = project_root / "src" / "config.mk"
    target_cfg   = target_dir / "config.mk"
    args_json    = target_dir / "modify_args.json"
    modify_script = scripts_dir / "modify_config.py"

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
    updater.apply_all()   # handles TECH_DIR, TECH_LEF, etc.
    updater.write()

    # 5) Create symlinks for all required resources
    #    Assume updater.symlink_pairs is a list of (src_path, dst_path)
    symlink_pairs = updater.symlink_pairs
    batch_symlink(symlink_pairs)

    logger.info("Platform generation finished successfully.")
