import unittest
from click.testing import CliRunner
from mock import patch

from tenx.app import TenxApp
from tenx.reads_cli import reads_cli, reads_download_cmd

class TenxRdsCliTest(unittest.TestCase):

    def setUp(self):
        if TenxApp.config is None: TenxApp()
        TenxApp.config["TENX_DATA_PATH"] = "/mnt/disks/data"
        TenxApp.config["TENX_REMOTE_URL"] = "gs://data"

    def tearDown(self):
        TenxApp.config = None

    def test0_reads_cli(self):
        runner = CliRunner()
        result = runner.invoke(reads_cli, ["--help"])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(reads_cli, [])
        self.assertEqual(result.exit_code, 0)

    @patch("tenx.reads.download")
    def test_reads_download(self, dl_p):
        runner = CliRunner()
        result = runner.invoke(reads_download_cmd, ["--help"])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(reads_download_cmd, [])
        self.assertEqual(result.exit_code, 2)

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
