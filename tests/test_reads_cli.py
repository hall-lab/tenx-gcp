import subprocess, unittest
from click.testing import CliRunner
from mock import patch

from tenx.app import TenxApp
from tenx.reads_cli import reads_cli, reads_download_cmd

class TenxRdsCliTest(unittest.TestCase):

    def test1_rds_cli(self):
        runner = CliRunner()
        result = runner.invoke(reads_cli, ["--help"])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(reads_cli, [])
        self.assertEqual(result.exit_code, 0)

    @patch("tenx.reads.download")
    def test2_tenx_reads_download(self, dl_p):
        runner = CliRunner()
        result = runner.invoke(reads_download_cmd, ["--help"])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(reads_download_cmd, [])
        self.assertEqual(result.exit_code, 2)

        result = runner.invoke(reads_download_cmd, ["MYSAMPLE"])
        self.assertEqual(result.exit_code, 1)

        TenxApp.config = {}
        result = runner.invoke(reads_download_cmd, ["MYSAMPLE"])
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        expected_output = ""
        self.assertEqual(result.output, expected_output)

# -- TenxRdsCliTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
