import io, os, sys, tempfile, unittest
from click.testing import CliRunner
from mock import patch

from tenx.app import TenxApp
from tenx.cli import cli
from tenx.aln_cli import aln_cli, aln_align_cmd, aln_upload_cmd
from tenx.sample import TenxSample
from tenx.reference import TenxReference

class AlnCliTest(unittest.TestCase):
    def setUp(self):
        self.temp_d = tempfile.TemporaryDirectory()
        if TenxApp.config is None: TenxApp()
        TenxApp.config = {
                "TENX_DATA_PATH": self.temp_d.name,
                "TENX_REMOTE_URL": "gs://data",
                "TENX_REMOTE_REFS_URL": "gs://data/refs",
                "TENX_ALN_VCMODE": "freebayes",
                "TENX_ALN_MODE": "wgs",
                "TENX_ALN_MEM": "1",
                "TENX_ALN_CORES": "1",
                }

        sample = TenxSample(name="__SAMPLE__", base_path=TenxApp.config["TENX_DATA_PATH"])
        ref = TenxReference(name="__REF__")
        self.aln= sample.alignment(ref)
        rsample = TenxSample(name="__SAMPLE__", base_path=TenxApp.config["TENX_REMOTE_URL"])
        self.raln = rsample.alignment(ref)

        os.chdir(self.temp_d.name)
        os.makedirs(self.aln.outs_path)
        os.makedirs(os.path.join(TenxApp.config["TENX_DATA_PATH"], "references"))

    def tearDown(self):
        self.temp_d.cleanup()
        TenxApp.config = None

    def test1_tenx_aln(self):
        runner = CliRunner()

        result = runner.invoke(aln_cli, ["--help"])
        self.assertEqual(result.exit_code, 0)

    import tenx.alignment
    @patch('tenx.alignment.run_align')
    def test2_tenx_aln_align(self, run_align_p):
        runner = CliRunner()

        result = runner.invoke(aln_align_cmd, ["--help"])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(aln_align_cmd, [])
        self.assertEqual(result.exit_code, 2)

        result = runner.invoke(aln_align_cmd, ["__SAMPLE__", "__REF__"])
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        expected_output = ""
        self.assertEqual(result.output, expected_output)
        run_align_p.assert_called_once()

    @patch('tenx.alignment.run_upload')
    def test2_tenx_aln_upload(self, run_upload_p):
        runner = CliRunner()
        result = runner.invoke(aln_upload_cmd, ["--help"])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(aln_upload_cmd, [])
        self.assertEqual(result.exit_code, 2)

        result = runner.invoke(aln_upload_cmd, ["__SAMPLE__"])
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        expected_output = ""
        self.assertEqual(result.output, expected_output)
        run_upload_p.assert_called_once()

# -- AlnCliTest

if __name__ == '__main__':
    unittest.main(verbosity=2)
