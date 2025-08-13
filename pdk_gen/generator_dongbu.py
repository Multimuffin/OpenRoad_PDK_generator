import logging
from pathlib import Path
from .setup_config import load_user_config
from .symlink_utils import batch_symlink
#from .config_updater import ConfigUpdater
from .config_updater_dongbu import ConfigUpdaterDongbu
from .ui_utils import list_dir
import shutil
import json

logger = logging.getLogger(__name__)

def generate_platform_dongbu(tech_name: str) -> None:
    """
    Orchestrates PDK platform generation for dongbu technology.
    Steps:
      1. Use provided base directory (il11sj or is18sh) from tech_name argument
      2. Automatically select relevant STD directory (without _G_ or _S_)
      3. Use selected STD directory as basis and name for new PDK
      4. Create platform folders
      5. Copy template and write args JSON
      6. Invoke ConfigUpdaterDongbu
      7. Create necessary symlinks
    """
    config = load_user_config()
    project_root = Path.cwd()
    platforms_dir = Path(config["platforms_root"])

    # 1) Use provided base directory (il11sj or is18sh)
    dongbu_root = config["tech_roots"]["dongbu"]
    base_path = Path(dongbu_root) / tech_name #/opt/tech/dbhitek/digital/il11sj

    # 2) Automatically select relevant STD directory (without _G_ or _S_)
    std_dirs = [d.name for d in base_path.iterdir() if d.is_dir() and d.name.startswith("DBH_STD") and "_G_" not in d.name and "_S_" not in d.name]
    std_g_dirs = [d.name for d in base_path.iterdir() if d.is_dir() and d.name.startswith("DBH_STD") and "_G_" in d.name]
    if not std_dirs and not std_g_dirs:
        logger.error(f"No valid STD directories found in {base_path}")
        return
    selected_std = std_dirs[0] if std_dirs else None
    selected_std_g = std_g_dirs[0] if std_g_dirs else None
    std_path = base_path / (selected_std or selected_std_g)

    # 3) Ask user for Metal Stack
    lef_tf_dir = std_path / "LEF" / "TF"
    metal_stack_files = [f.name for f in lef_tf_dir.glob("*_TECH.lef") if f.is_file()]
    stack_options = []
    for fname in metal_stack_files:
        # Extract e.g. '3M' from 'DBH_1533IL11SJ_GE1P5V_3M_TECH.lef'
        parts = fname.split('_')
        for part in parts:
            if part.endswith('M') and part[:-1].isdigit():
                stack_options.append(part)
                break
    if not stack_options:
        logger.error(f"No metal stack options found in {lef_tf_dir}")
        return
    m_stack = list_dir(stack_options, title="Available Metal Stacks")

    # 3) Use selected STD directory as basis and name for new PDK
    target_dir = platforms_dir / f"{selected_std}_{m_stack}"
    print(f"Creating platform directory: {target_dir}")

    args_json    = target_dir / "modify_args.json"

    # 4) Create (or empty) target directory
    if target_dir.exists():
        logger.info(f"Overwriting existing platform directory: {target_dir}")
    else:
        logger.info(f"Creating platform directory: {target_dir}")
        target_dir.mkdir(parents=True, exist_ok=True)

    # 5) Copy templates
    logger.info(f"Copying template config.mk to {target_dir / 'config.mk'}")
    shutil.copy2(project_root / "src" / "dongbu" / "config.mk", target_dir / "config.mk")
    logger.info(f"Copying template gds2.map to {target_dir / 'gds2.map'}")
    shutil.copy2(project_root / "src" / "dongbu" / "gds2.map", target_dir / "gds2.map")
    logger.info(f"Copying template constraint.sdc to {target_dir / 'constraint.sdc'}")
    shutil.copy2(project_root / "src" / "dongbu" / "constraint.sdc", target_dir / "constraint.sdc")
    logger.info(f"Copying template fastroute.tcl to {target_dir / 'fastroute.tcl'}")
    shutil.copy2(project_root / "src" / "dongbu" / "fastroute.tcl", target_dir / "fastroute.tcl")
    logger.info(f"Copying template il11sj.lyp to {target_dir / 'il11sj.lyp'}")
    shutil.copy2(project_root / "src" / "dongbu" / "il11sj.lyp", target_dir / "il11sj.lyp")
    logger.info(f"Copying template il11sj.lyt to {target_dir / 'il11sj.lyt'}")
    shutil.copy2(project_root / "src" / "dongbu" / "il11sj.lyt", target_dir / "il11sj.lyt")
    logger.info(f"Copying template make_tracks.tcl to {target_dir / 'make_tracks.tcl'}")
    shutil.copy2(project_root / "src" / "dongbu" / "make_tracks.tcl", target_dir / "make_tracks.tcl")
    logger.info(f"Copying template pdn.tcl to {target_dir / 'pdn.tcl'}")
    shutil.copy2(project_root / "src" / "dongbu" / "pdn.tcl", target_dir / "pdn.tcl")
    logger.info(f"Copying template setRC.tcl to {target_dir / 'setRC.tcl'}")
    shutil.copy2(project_root / "src" / "dongbu" / "setRC.tcl", target_dir / "setRC.tcl")


    template_cfg = project_root / "src" / "dongbu" / "config.mk"
    target_cfg   = target_dir / "config.mk"

    payload = {
        "platform_name": selected_std,
        "generation_script_directory": str(project_root / "scripts"),
        "project_root": str(project_root),
        "platforms_dir": str(platforms_dir),
        "new_platform": str(target_dir),
        "config_template": str(template_cfg),
        "config_file": str(target_cfg),
        "technology": "dongbu",
        "dongbu_base": tech_name,
        "dongbu_std": selected_std,
        "dongbu_std_g": selected_std_g,
        "base_path": str(base_path),
        "metal": str(m_stack)
    }
    logger.debug(f"Writing modify_args.json: {payload}")
    with args_json.open("w") as f:
        json.dump(payload, f, indent=2)

    # 6) Update config.mk via ConfigUpdaterDongbu
    updater = ConfigUpdaterDongbu(cfg_path=target_cfg, args_path=args_json)
    updater.load()
    updater.apply_all()
    updater.write()

    # 7) Create symlinks for all required resources
    symlink_pairs = updater.symlink_pairs
    batch_symlink(symlink_pairs)

    logger.info("Dongbu platform generation finished successfully.")
