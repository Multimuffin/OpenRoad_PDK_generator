import json
import re
from pathlib import Path
import logging
from pdk_gen.dir_utils import create_platform_dirs
from pdk_gen.file_finder import find_lib_files_by_corner
from pdk_gen.ui_utils import list_dir
from pdk_gen.symlink_utils import handle_resource, cell_name_with_wb
from pdk_gen.lef_utils import find_macros_in_lef

#from pdk_gen.symlink_utils import create_symlink


logger = logging.getLogger(__name__)

class ConfigUpdaterDongbu:
    """
    Dongbu-spezifischer ConfigUpdater.
    Lädt config.mk und modify_args.json, aktualisiert die Export-Variablen und sammelt Symlink-Aufgaben.
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
        Dongbu-spezifische Anpassungen für config.mk und Symlinks.
        """
        plat   = self.args["platform_name"]
        new_pl = Path(self.args["new_platform"])
        m_stack = self.args.get("metal")
        std_g = self.args["dongbu_std_g"]
        tech_root = self.args.get("base_path")

        # Dongbu: create platform directories
        create_platform_dirs(new_pl)
        dongbu_lef_dir = new_pl / "lef"
        dongbu_lef_dir.mkdir(parents=True, exist_ok=True)
        dongbu_lib_dir = new_pl / "lib"
        dongbu_lib_dir.mkdir(parents=True, exist_ok=True)
        dongbu_gds_dir = new_pl / "gds"
        dongbu_gds_dir.mkdir(parents=True, exist_ok=True)
        dongbu_cdl_dir = new_pl / "cdl"
        dongbu_cdl_dir.mkdir(parents=True, exist_ok=True)

################################################################################
#                                   TECH/LIBS                                  #
################################################################################

        # Dongbu: TECH_DIR
        if not tech_root:
            raise RuntimeError("Missing tech_root in args: cannot build TECH_DIR!")
        tech_dir = Path(tech_root) / plat
        self._update_export("TECH_DIR", [tech_dir])
        self._update_export("TECH_GDS_DIR", [dongbu_gds_dir])
        self._update_export("TECH_CDL_DIR", [dongbu_cdl_dir])

        # Dongbu: LEF
        lef_src_dir = tech_dir / "LEF"
        print(f"Using LEF source directory: {lef_src_dir}")
        print(f"Metal Stack: {m_stack}")
        handle_resource(lef_src_dir / "TF", dongbu_lef_dir, f"*{m_stack}_TECH.lef", "TECH_LEF", self)
        handle_resource(lef_src_dir, dongbu_lef_dir, "*.lef", "SC_LEF", self)

        # Dongbu: LIB
        lib_src_dir = tech_dir / "LIBERTY"
        corners = ["TT", "SS", "FF"]
        all_lib_paths = []
        for corner in corners:
            pattern = f"*{corner}*.lib"
            files = list(lib_src_dir.glob(pattern))
            if not files:
                print(f"Keine LIB-Dateien für Corner {corner} gefunden!")
                continue
            for file in files:
                dst = dongbu_lib_dir / file.name
                from pdk_gen.symlink_utils import create_symlink
                create_symlink(file, dst)
                all_lib_paths.append(dst)
        if all_lib_paths:
            self._update_export("LIB_FILES", all_lib_paths)
        else:
            print("Keine LIB-Dateien gefunden!")

        # Dongbu: GDS
        gds_src_dir = Path(tech_root) / std_g / "GDS"
        handle_resource(gds_src_dir, dongbu_gds_dir, "*.gds", "GDS_FILE", self)
        handle_resource(gds_src_dir, dongbu_gds_dir, "*.map", "GDS_LAYER_MAP", self)

        # Dongbu: CDL
        cdl_src_dir = Path(tech_root) / std_g / "CDL"
        handle_resource(cdl_src_dir, dongbu_cdl_dir, "*.cdl", "CDL_FILE", self, ask_user=True, ui_title="CDL-Files")

################################################################################
#                               Synth Variables                                #
################################################################################

        self._update_export("ABC_DRIVER_CELL", ["NID2"])
        self._update_export("TIEHI_CELL_AND_PORT", ["TIEH Z"])
        self._update_export("TIELO_CELL_AND_PORT", ["TIEL Z"])
        self._update_export("MIN_BUF_CELL_AND_PORTS", ["NID0 A Z"])

################################################################################
#                                  Floorplan                                   #
################################################################################

        if str(m_stack).startswith('M3'):
            self._update_export("IO_PLACER_H", ["M3"])
            self._update_export("IO_PLACER_V", ["M2"])
        else:
            self._update_export("IO_PLACER_H", ["M3"])
            self._update_export("IO_PLACER_V", ["M4"])

################################################################################
#                                    Place                                     #
################################################################################

################################################################################
#                                     CTS                                      #
################################################################################

        sc_lef = [f for f in dongbu_lef_dir.glob("*.lef") if f"_{m_stack}_" not in f.name]
        self._update_export("FILL_CELLS", [find_macros_in_lef(next(iter(sc_lef)), "FILL")])


################################################################################
#                                    Route                                     #
################################################################################

        self._update_export("MAX_ROUTING_LAYER", ["M" + str(m_stack)[0]])



################################################################################
#                                   IR Drop                                    #
################################################################################




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
        from pdk_gen.file_finder import find_first
        result = find_first(directory, pattern)
        if result is None:
            raise FileNotFoundError(f"No files '{pattern}' in {directory}")
        return result
