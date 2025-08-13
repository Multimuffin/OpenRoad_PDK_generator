import json
#import re
from pathlib import Path
import logging
from pdk_gen.dir_utils import create_platform_dirs
#from pdk_gen.file_finder import find_lib_files_by_corner
#from pdk_gen.ui_utils import list_dir
from pdk_gen.symlink_utils import handle_resource, cell_name_with_wb
from pdk_gen.lef_utils import find_macros_in_lef

#from pdk_gen.symlink_utils import create_symlink


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

    def apply_all(self, metal_subdir: str = None) -> None:
        """
        Compute all updated export lines and symlink tasks:
          - TECH_DIR
          - TECH_GDS_DIR, TECH_CDL_DIR, TECH_LEF, SC_LEF
          - LIB_FILES, GDS_LAYER_MAP, CDL_FILE
        Set TECH_LEF to symlink 'metal_stack.lef' pointing to selected LEF.
        """
        plat   = self.args["platform_name"]
        # root   = Path(self.args["project_root"])
        # scripts= Path(self.args["generation_script_directory"])
        root   = Path.cwd()  # <--- changed for robust path handling
        scripts= root / "scripts"
        new_pl = Path(self.args["new_platform"])
        m_stack = self.args.get("m_stack")
        
        # create platform directories
        create_platform_dirs(new_pl)
        mlef_dir = new_pl / "lef" / "mlef"
        sclef_dir = new_pl / "lef" / "sclef"
        mlef_dir.mkdir(parents=True, exist_ok=True)
        sclef_dir.mkdir(parents=True, exist_ok=True)

################################################################################
#                                   TECH/LIBS                                  #
################################################################################
        # new TECH_DIR
        tech_root = self.args.get("tech_root")
        if not tech_root:
            raise RuntimeError("Missing tech_root in args: cannot build TECH_DIR!")
        tech_dir = Path(tech_root) / plat
        self._update_export("TECH_DIR", [tech_dir])

        self._update_export("TECH_GDS_DIR", [new_pl / "gds"])
        self._update_export("TECH_CDL_DIR", [new_pl / "cdl"])

        # new SC_LEF
        sc_src_dir = tech_dir / "lib" / "lef"
        handle_resource(sc_src_dir, sclef_dir, "*.lef", "SC_LEF", self)

        # new TECH_LEF
        if metal_subdir:
            mlef_src_dir = tech_dir / "tech" / metal_subdir / "lef" / m_stack
        else:
            mlef_src_dir = tech_dir / "tech" / "lef" / m_stack
        handle_resource(mlef_src_dir, mlef_dir, "*.lef", "TECH_LEF", self)
        print("TECH_LEF Pfade:", list(mlef_dir.glob("*.lef")))
        print("SC_LEF Pfade:", list(sclef_dir.glob("*.lef")))

        # new LIB_FILES
        lib_src_dir = tech_dir / "lib" / "liberty"
        lib_dst_dir = new_pl / "lib"
        lib_dst_dir.mkdir(parents=True, exist_ok=True)
        corners = ["ff", "ss", "tt"]
        all_lib_paths = []
        for corner in corners:
            paths = handle_resource(lib_src_dir, lib_dst_dir, f"*{corner}*.lib", "LIB_FILES", self, ask_user=True, ui_title=f"LIB-Files for Corner '{corner}'", return_only=True)
            all_lib_paths.extend(str(p) for p in paths)
        self._update_export("LIB_FILES", all_lib_paths)

        # new GDS_LAYER_MAP
        if metal_subdir:
            gds_map_src_dir = tech_dir / "tech" / metal_subdir / "lef" / m_stack
        else:
            gds_map_src_dir = tech_dir / "tech" / "lef" / m_stack
        handle_resource(gds_map_src_dir, new_pl / "gds", "*.map", "GDS_LAYER_MAP", self)

        # new CDL_FILE
        cdl_src_dir = tech_dir / "lib" / "cdl"
        cdl_dst_dir = new_pl / "cdl"
        cdl_dst_dir.mkdir(parents=True, exist_ok=True)
        handle_resource(cdl_src_dir, cdl_dst_dir, "*.cdl", "CDL_FILE", self, ask_user=True, ui_title="CDL-Dateien")
 
        # new GDS_FILE
        gds_src_dir = tech_dir / "lib" / "gds"
        gds_dst_dir = new_pl / "gds"
        gds_dst_dir.mkdir(parents=True, exist_ok=True)
        handle_resource(gds_src_dir, gds_dst_dir, "*.gds", "GDS_FILE", self)

################################################################################
#                               Synth Variables                                #
################################################################################
        
 
        self._update_export("ABC_DRIVER_CELL", [cell_name_with_wb(plat, "BUF_X8_18_SVT")])
        self._update_export("TIEHI_CELL_AND_PORT", [cell_name_with_wb(plat, "TIEH_18_SVT", "", "Q")])
        self._update_export("TIELO_CELL_AND_PORT", [cell_name_with_wb(plat, "TIEL_18_SVT", "", "Q")])
        self._update_export("MIN_BUF_CELL_AND_PORTS", [cell_name_with_wb(plat, "BUF_X2_18_SVT", "", "A", "Q")])

################################################################################
#                                  Floorplan                                   #
################################################################################

        if str(m_stack).startswith('3'):
            self._update_export("IO_PLACER_H", ["TOP_M"])
        elif str(m_stack).startswith('2'):
            self._update_export("IO_PLACER_H", ["M1"])
            self._update_export("IO_PLACER_V", ["TOP_M"])

        self._update_export("TAP_CELL_NAME", [cell_name_with_wb(plat, "FILLTIE_18_SVT")])


################################################################################
#                                    Place                                     #
################################################################################



################################################################################
#                                     CTS                                      #
################################################################################

        self._update_export("FILL_CELLS", [find_macros_in_lef(next(sclef_dir.glob("*.lef")), "FILLER_")])

################################################################################
#                                    Route                                     #
################################################################################



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
