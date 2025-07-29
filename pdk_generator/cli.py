import sys
import logging
import click

from pdk_generator.generator import generate_platform

# configure root logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

@click.command()
@click.argument("tech_name")
@click.option("--verbose", is_flag=True, help="Enable debug logging.")
def main(tech_name: str, verbose: bool):
    """
    Kick off PDK platform generation for TECH_NAME.
    """
    if verbose:
        logger.setLevel(logging.DEBUG)
        logging.getLogger('pdk_generator').setLevel(logging.DEBUG)
        logger.debug("Debug logging enabled")

    try:
        logger.info(f"Starting PDK generation for '{tech_name}'...")
        generate_platform(tech_name)
        logger.info("PDK generation completed successfully.")
    except Exception as e:
        logger.error(f"Error during generation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
