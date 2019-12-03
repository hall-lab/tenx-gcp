import subprocess, tempfile, unittest
from click.testing import CliRunner
from mock import patch

from tenx.app import TenxApp
from tenx.asm_download import asm_download_cmd

class TenxAsmDownloadTest(unittest.TestCase):
    def setUp(self):
        self.temp_d = tempfile.TemporaryDirectory()
        TenxApp()
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
            self.maxDiff = 10000000000
            expected_output = "\n".join([
                "Download assembly ... ",
                "Sample: __TESTER__",
                "Assembly directory: /tmp/__TESTER__/assembly",
                "Assembly remote url: gs://data/__TESTER__/assembly",
                "RUNNING: gsutil -m cp gs://data/__TESTER__/assembly/_perf gs://data/__TESTER__/assembly/_log .",
                "RUNNING: gsutil -m cp gs://data/__TESTER__/assembly/outs/report.txt gs://data/__TESTER__/assembly/outs/summary.csv .",
                "RUNNING: gsutil -m rsync -r gs://data/__TESTER__/assembly/mkoutput .",
                "Download assembly ... DONE",
                "",
            ])
            self.assertEqual(result.output, expected_output)
        except:
            print(result.output)
            raise

# -- TenxAsmCliTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
