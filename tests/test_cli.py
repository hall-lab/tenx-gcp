import subprocess, unittest
from click.testing import CliRunner

from tenx.cli import cli

class TenxCliTest(unittest.TestCase):

    def test1_cli(self):
        runner = CliRunner()
        result = runner.invoke(cli, [])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ["--help"])
        self.assertEqual(result.exit_code, 0)

# -- TenxCliTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
