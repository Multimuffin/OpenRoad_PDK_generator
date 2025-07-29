from click.testing import CliRunner
from pdk_generator.cli import main

def test_cli_help():
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "Usage" in result.output

def test_cli_invalid(tmp_path, monkeypatch):
    # simulate generate_platform raising
    monkeypatch.setenv("PYTHONPATH", str(Path(__file__).parent.parent))
    def fake_generate(name):
        raise RuntimeError("oops")
    monkeypatch.setattr("pdk_generator.generator.generate_platform", fake_generate)

    runner = CliRunner()
    result = runner.invoke(main, ["techX"])
    assert result.exit_code != 0
    assert "Error during generation: oops" in result.output
