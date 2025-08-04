import sys
import logging
import click
from pathlib import Path
from .setup_config import load_user_config

from .generator import generate_platform
from .ui_utils import list_dir

# configure root logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

@click.command()
@click.argument("tech_name", required=False)
@click.option("--verbose", is_flag=True, help="Enable debug logging.")
def main(tech_name: str, verbose: bool):
    """
    Kick off PDK platform generation for TECH_NAME.
    If no TECH_NAME is given, show a list and let the user select interactively.
    """
    if verbose:
        logger.setLevel(logging.DEBUG)
        logging.getLogger('pdk_generator').setLevel(logging.DEBUG)
        logger.debug("Debug logging enabled")

    try:
        config = load_user_config()
    except Exception:
        print("Bitte zuerst 'pdk-setup' ausführen, um die Pfade zu konfigurieren!")
        sys.exit(1)

    tech_root = config["tech_root"]
    # platforms_root = config["platforms_root"]  # falls benötigt

    if not tech_name:
        tech_name = list_dir(tech_root, title="Available Technologies")

    tech_lef_base = Path(tech_root) / tech_name / "tech"
    direct_lef = tech_lef_base / "lef"
    try:
        if direct_lef.is_dir():
            m_stack = list_dir(direct_lef, title="Available Metal Stacks")
            logger.info(f"Starting PDK generation for '{tech_name}' with metal stack '{m_stack}'...")
            generate_platform(tech_name, m_stack)
        else:
            subdirs = [d for d in tech_lef_base.iterdir() if d.is_dir() and (d / "lef").is_dir()]
            if not subdirs:
                click.echo(f"No valid metal stack directories found for {tech_name}.", err=True)
                sys.exit(1)
            sel_mtlsub = list_dir([d.name for d in subdirs], title="Select subdirectory for Metal Stack")
            mtlsubdir = next(d for d in subdirs if d.name == sel_mtlsub)
            m_stack = list_dir(mtlsubdir / "lef", title="Available Metal Stacks")
            logger.info(f"Starting PDK generation for '{tech_name}' with metal stack '{m_stack}'...")
            generate_platform(tech_name, m_stack, metal_subdir=mtlsubdir.name)
        logger.info("PDK generation completed successfully.")

    except Exception as e:
        logger.error(f"Error during generation: {e}")
        click.echo(f"Error during generation: {e}", err=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
