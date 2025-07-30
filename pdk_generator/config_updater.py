import json
import re
from pathlib import Path
import logging
from pdk_generator.dir_utils import create_platform_dirs

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
        self.m_stack = None

    def load(self) -> None:
        """Read config.mk and JSON args into memory."""
        logger.debug(f"Loading config file: {self.cfg_path}")
        self.lines = self.cfg_path.read_text().splitlines(keepends=True)
        logger.debug(f"Loading args file: {self.args_path}")
        self.args = json.loads(self.args_path.read_text())
        self.m_stack = self.args.get("m_stack")

    def apply_all(self) -> None:
        """
        Compute all updated export lines and symlink tasks:
          - TECH_DIR
          - TECH_GDS_DIR, TECH_CDL_DIR, TECH_LEF, SC_LEF
          - LIB_FILES, GDS_LAYER_MAP, CDL_FILE
        Set TECH_LEF to symlink 'metal_stack.lef' pointing to selected LEF.
        """
        plat   = self.args["platform_name"]
        root   = Path(self.args["project_root"])
        scripts= Path(self.args["generation_script_directory"])
        new_pl = Path(self.args["new_platform"])
        m_stack = self.args.get("m_stack")

        # create platform directories
        create_platform_dirs(new_pl)
        mlef_dir = new_pl / "lef" / "mlef"
        sclef_dir = new_pl / "lef" / "sclef"
        mlef_dir.mkdir(parents=True, exist_ok=True)
        sclef_dir.mkdir(parents=True, exist_ok=True)

        # new TECH_DIR
        tech_dir = Path(f"/opt/tech/tower/digital/{plat}")
        self._update_export("TECH_DIR", [tech_dir])

        self._update_export("TECH_GDS_DIR", [new_pl / "gds"])
        self._update_export("TECH_CDL_DIR", [new_pl / "cdl"])

        # new SC_LEF
        sc_src_dir = tech_dir / "lib" / "lef"
        for lef_file in sc_src_dir.glob("*.lef"):
            dst = sclef_dir / lef_file.name
            self.symlink_pairs.append((lef_file, dst))

        # new TECH_LEF
        mlef_src_dir = tech_dir / "tech" / "lef" / m_stack
        for lef_file in mlef_src_dir.glob("*.lef"):
            dst = mlef_dir / lef_file.name
            self.symlink_pairs.append((lef_file, dst))


        mlef_files = list(mlef_dir.glob("*.lef"))
        sclef_files = list(sclef_dir.glob("*.lef"))
        if len(mlef_files) == 1:
            self._update_export("TECH_LEF", [mlef_files[0]])
        else:
            self._update_export("TECH_LEF", mlef_files)
        if len(sclef_files) == 1:
            self._update_export("SC_LEF", [sclef_files[0]])
        else:
            self._update_export("SC_LEF", sclef_files)

        # LIB-Files: Interaktive Auswahl durch den Nutzer
        lib_src_dir = tech_dir / "lib" / "liberty"
        available_libs = list(lib_src_dir.glob("*.lib"))
        selected_libs = []
        print("Verfügbare LIB-Dateien:")
        for idx, libfile in enumerate(available_libs):
            print(f"[{idx}] {libfile.name}")
        user_input = input("Bitte die gewünschten LIB-Dateien durch Komma getrennt auswählen (z.B. 0,2,3): ")
        try:
            indices = [int(i.strip()) for i in user_input.split(",") if i.strip().isdigit()]
            for i in indices:
                if 0 <= i < len(available_libs):
                    selected_libs.append(available_libs[i])
        except Exception as e:
            print(f"Fehler bei der Auswahl: {e}")
        if selected_libs:
            self._update_export("LIB_FILES", selected_libs)
        else:
            print("Keine LIB-Dateien ausgewählt!")

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
