import json
import re
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class ConfigUpdater:
    """
    Load a config.mk template and a JSON args file,
    update the export variables, and collect symlink tasks.
    """
    def __init__(self, cfg_path: Path, args_path: Path):
        self.cfg_path = Path(cfg_path)
        self.args_path = Path(args_path)
        self.lines: list[str] = []
        self.args: dict = {}
        self.symlink_pairs: list[tuple[Path, Path]] = []

    def load(self) -> None:
        """Read config.mk and JSON args into memory."""
        logger.debug(f"Loading config file: {self.cfg_path}")
        self.lines = self.cfg_path.read_text().splitlines(keepends=True)
        logger.debug(f"Loading args file: {self.args_path}")
        self.args = json.loads(self.args_path.read_text())

    def apply_all(self) -> None:
        """
        Compute all updated export lines and symlink tasks:
          - TECH_DIR
          - TECH_GDS_DIR, TECH_CDL_DIR, TECH_LEF, SC_LEF
          - LIB_FILES, GDS_LAYER_MAP, CDL_FILE
        """
        plat   = self.args["platform_name"]
        root   = Path(self.args["project_root"])
        scripts= Path(self.args["generation_script_directory"])
        new_pl = Path(self.args["new_platform"])

        # compute new TECH_DIR
        tech_dir = Path(f"/opt/tech/tower/digital/{plat}")
        self._update_export("TECH_DIR", [tech_dir])
        # later on, add symlink for TECH_DIR if needed

        # collect LEF & SC_LEF
        lef_src    = (tech_dir / "lib" / "lef")
        metal_src  = self._find_first(lef_src, "*.lef")
        sc_src     = self._find_first(lef_src, "*.lef")
        # destination under new_pl/lef
        metal_dst  = new_pl / "lef" / metal_src.name
        sc_dst     = new_pl / "lef" / sc_src.name
        self._update_export("TECH_LEF", [metal_dst])
        self._update_export("SC_LEF",   [sc_dst])
        self.symlink_pairs += [(metal_src, metal_dst), (sc_src, sc_dst)]

        # TODO: compute and update GDS, CDL, LIB_FILES, etc. similarly

    def write(self) -> None:
        """Write updated lines back to config.mk."""
        logger.debug(f"Writing updated config to {self.cfg_path}")
        self.cfg_path.write_text("".join(self.lines))

    def _update_export(self, key: str, paths: list[Path]) -> None:
        """
        Update or append 'export KEY = ...' lines in self.lines.
        Single path: one-liner; multiple: backslash continuation.
        """
        prefix = f"export {key}"
        new_block = []
        if len(paths) == 1:
            new_block.append(f"{prefix} = {paths[0]}\n")
        else:
            new_block.append(f"{prefix} = {paths[0]} \\\n")
            for p in paths[1:]:
                new_block.append(f"\t{p} \\\n")

        # find and replace existing block
        i = 0
        while i < len(self.lines):
            if self.lines[i].startswith(prefix):
                j = i + 1
                while j < len(self.lines) and self.lines[j].rstrip().endswith("\\"):
                    j += 1
                # replace lines[i:j] with new_block
                self.lines[i:j] = new_block
                return
            i += 1

        # if not found, append at end
        self.lines.extend(new_block)

    def _find_first(self, directory: Path, pattern: str) -> Path:
        """Helper to find the first file matching pattern, or raise."""
        from pdk_generator.file_finder import find_first
        result = find_first(directory, pattern)
        if result is None:
            raise FileNotFoundError(f"No files '{pattern}' in {directory}")
        return result
