import unittest
from pathlib import Path
import json
from pdk_gen.config_updater import ConfigUpdater

SAMPLE_CFG = """
export FOO = old
export BAR = old1 \\
    old2 \\
"""

class TestConfigUpdater(unittest.TestCase):
    def setUp(self):
        import tempfile
        self.tmpdir = tempfile.TemporaryDirectory()
        self.tmp_path = Path(self.tmpdir.name)
        self.cfg_file = self.tmp_path / "config.mk"
        self.cfg_file.write_text(SAMPLE_CFG)
        self.args = {
            "platform_name": "techA",
            "project_root": str(self.tmp_path),
            "generation_script_directory": str(self.tmp_path),
            "new_platform": str(self.tmp_path),
        }
        self.args_file = self.tmp_path / "args.json"
        self.args_file.write_text(json.dumps(self.args))
        print(f"Temporary directory created at: {self.tmp_path}")   

    def tearDown(self):
        self.tmpdir.cleanup()
        print(f"Temporary directory {self.tmp_path} cleaned up.")

    def test_update_export_and_write(self):
        upd = ConfigUpdater(self.cfg_file, self.args_file)
        upd.load()
        upd._update_export("FOO", [Path("/opt/new")])
        upd._update_export("BAR", [Path("a"), Path("b")])
        upd.write()
        text = self.cfg_file.read_text()
        self.assertIn("export FOO = /opt/new", text)
        self.assertIn("export BAR = a \\", text)
        self.assertIn("\tb \\", text)
        print("test_update_export_and_write successful!")

if __name__ == "__main__":
    unittest.main()
