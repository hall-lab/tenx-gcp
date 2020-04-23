import os, subprocess, tempfile, unittest
from click.testing import CliRunner
from mock import patch

from tenx.app import TenxApp
from tenx.asm_download import asm_download_cmd

class TenxAsmDownloadTest(unittest.TestCase):
    def setUp(self):
        self.temp_d = tempfile.TemporaryDirectory()
        os.chdir(self.temp_d.name)
        TenxApp.config = {}
        TenxApp.config['TENX_DATA_PATH'] = "/tmp"
        TenxApp.config['TENX_REMOTE_URL'] = 'gs://data'

    def tearDown(self):
        self.temp_d.cleanup()

    @patch('subprocess.check_call')
    def test_asm_download(self, check_call_call_patch):
        check_call_call_patch.return_value = 1
        runner = CliRunner()

        result = runner.invoke(asm_download_cmd, ["--help"])
        self.assertEqual(result.exit_code, 0)

        sample_name = "__TESTER__"
        result = runner.invoke(asm_download_cmd, [sample_name])
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        self.maxDiff = 10000000000
        expected_output = "\n".join([
            "Download assembly ... ",
            "Remote path: gs://data/__TESTER__/assembly",
            "Local path: /tmp/__TESTER__/assembly",
            "RUNNING: gsutil -m rsync -r gs://data/__TESTER__/assembly .",
            "Download assembly ... DONE",
            "",
        ])
        self.assertEqual(result.output, expected_output)

# -- TenxAsmCliTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
