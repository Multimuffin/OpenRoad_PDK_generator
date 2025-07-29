from pathlib import Path
import json
import pytest
from pdk_generator.config_updater import ConfigUpdater

SAMPLE_CFG = """
export FOO = old
export BAR = old1 \\
    old2 \\
"""

@pytest.fixture
def cfg_file(tmp_path):
    f = tmp_path / "config.mk"
    f.write_text(SAMPLE_CFG)
    args = {
        "platform_name": "techA",
        "project_root": str(tmp_path),
        "generation_script_directory": str(tmp_path),
        "new_platform": str(tmp_path),
    }
    (tmp_path / "args.json").write_text(json.dumps(args))
    return f, tmp_path / "args.json"

def test_update_export_and_write(cfg_file):
    cfg_path, args_path = cfg_file
    upd = ConfigUpdater(cfg_path, args_path)
    upd.load()
    upd._update_export("FOO", [Path("/opt/new")])
    upd._update_export("BAR", [Path("a"), Path("b")])
    upd.write()
    text = cfg_path.read_text()
    assert "export FOO = /opt/new" in text
    assert "export BAR = a \\" in text
    assert "\tb \\" in text
