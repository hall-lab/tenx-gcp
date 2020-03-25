import subprocess, unittest
from click.testing import CliRunner
from mock import patch

from tenx.list import remote_sample_names, remote_sample_details, list_cmd
from tenx.app import TenxApp

class ListTest(unittest.TestCase):
    def setUp(self):
        TenxApp()
        TenxApp.config = {"TENX_REMOTE_URL": "gs://data"}
        #TenxApp.config['TENX_REMOTE_URL'] = "gs://data"

    def tearDown(self):
        TenxApp.config = None

    @patch("subprocess.check_output")
    def test1_remote_samples(self, check_output_patch):
        check_output_patch.return_value = bytes("gs://data/SAMPLE1/\ngs://data/SAMPLE2/\ngs://data/SAMPLE3/", "utf-8")
        expected_sample_names = ["SAMPLE1", "SAMPLE2", "SAMPLE3"]
        sample_names = remote_sample_names()
        self.assertEqual(sample_names, expected_sample_names)

    @patch("subprocess.check_output")
    def test1_remote_sample_details(self, check_output_patch):
        check_output_patch.return_value = bytes("gs://data/SAMPLE3\ngs://data/SAMPLE3/alignment/\ngs://data/SAMPLE3/assembly/\ngs://data/SAMPLE3/reads/", "utf-8")
        expected_samples = {"SAMPLE3": {"alignment": "Y", "assembly": "Y", "reads": "Y",}}
        samples = remote_sample_details(expected_samples.keys())
        self.assertDictEqual(samples, expected_samples)

    @patch("tenx.list.remote_sample_names")
    @patch("tenx.list.remote_sample_details")
    def test2_asm_list_cmd_test(self, details_patch, names_patch):
        runner = CliRunner()
        result = runner.invoke(list_cmd, ["--help"])
        self.assertEqual(result.exit_code, 0)

        details_patch.return_value = {"SAMPLE3": {"alignment": "N", "assembly": "Y", "reads": "Y"}}
        result = runner.invoke(list_cmd, [])
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        expected_output = """SAMPLE_NAME    TYPE    ALN    ASM    RDS
-------------  ------  -----  -----  -----
SAMPLE3        REMOTE  N      Y      Y
"""
        self.assertEqual(result.output, expected_output)

# -- ListTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
