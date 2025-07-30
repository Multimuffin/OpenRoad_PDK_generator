import sys
import logging
import click
from pathlib import Path

from pdk_generator.generator import generate_platform
from pdk_generator.ui_utils import list_dir

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

    if not tech_name:
        tech_root = "/opt/tech/tower/digital/"
        tech_name = list_dir(tech_root, title="Available Technologies")


    tech_lef_base = Path(f"/opt/tech/tower/digital/{tech_name}/tech")
    direct_lef = tech_lef_base / "lef"
    if direct_lef.is_dir():
        m_stack = list_dir(direct_lef, title="Available Metal Stacks")
    else:
        subdirs = [d for d in tech_lef_base.iterdir() if d.is_dir() and (d / "lef").is_dir()]
        if not subdirs:
            click.echo(f"No valid metal stack directories found for {tech_name}.", err=True)
            sys.exit(1)
        selected = list_dir([d.name for d in subdirs], title="Select subdirectory for Metal Stack")
        selected_dir = next(d for d in subdirs if d.name == selected)
        m_stack = list_dir(selected_dir / "lef", title="Available Metal Stacks")

    try:
        logger.info(f"Starting PDK generation for '{tech_name}' with metal stack '{m_stack}'...")
        generate_platform(tech_name, m_stack)
        logger.info("PDK generation completed successfully.")
    except Exception as e:
        logger.error(f"Error during generation: {e}")
        click.echo(f"Error during generation: {e}", err=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
