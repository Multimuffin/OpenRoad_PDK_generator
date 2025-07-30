import unittest
from click.testing import CliRunner
from unittest.mock import patch
import sys

import pdk_generator.cli as cli_mod

class TestCLI(unittest.TestCase):
    def test_cli_help(self):
        """`pdk-gen --help` should exit 0 and show Usage."""
        runner = CliRunner()
        result = runner.invoke(cli_mod.main, ["--help"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Usage", result.output)

    # def test_cli_invalid(self):
    #     """If generate_platform raises, CLI should catch and exit !=0 with the error message."""
    #     # Patch sys.exit to raise SystemExit, so CliRunner catches it as nonzero exit code
    #     with patch("pdk_generator.generator.generate_platform", side_effect=RuntimeError("oops")), \
    #          patch("sys.exit", side_effect=SystemExit):
    #         runner = CliRunner()
    #         result = runner.invoke(cli_mod.main, ["tsl18fs190svt_Rev_2019.09"])
    #         self.assertNotEqual(result.exit_code, 0)
    #         self.assertIn("Error during generation: oops", result.output)

if __name__ == "__main__":
    unittest.main()
