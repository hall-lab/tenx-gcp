import io, os, subprocess, sys, tempfile, unittest
from click.testing import CliRunner
from mock import patch

from tenx.app import TenxApp
from tenx.asm_upload import asm_upload_cmd, run_upload
from tenx.sample import TenxSample

class AsmUploadTest(unittest.TestCase):

    def setUp(self):
        self.temp_d = tempfile.TemporaryDirectory()
        self.rurl = "gs://data"
        os.chdir(self.temp_d.name)
        sample = TenxSample(name='TESTER', base_path=self.temp_d.name)
        self.asm = sample.assembly()
        rsample = TenxSample(name='TESTER', base_path=self.rurl)
        self.remote_asm = rsample.assembly()
        if TenxApp.config is None: TenxApp()
        TenxApp.config['TENX_DATA_PATH'] = self.temp_d.name
        TenxApp.config['TENX_REMOTE_URL'] = self.rurl

    def tearDown(self):
        self.temp_d.cleanup()
        TenxApp.config = None

    @patch('subprocess.check_call')
    @patch("tenx.util.verify_upload")
    def test_asm_upload_cmd(self, verify_ul_patch, check_call_patch):
        runner = CliRunner()
        result = runner.invoke(asm_upload_cmd, ["--help"])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(asm_upload_cmd, [])
        self.assertEqual(result.exit_code, 2)

        os.makedirs(self.asm.outs_assembly_path)

        result = runner.invoke(asm_upload_cmd, ["TESTER"])
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise

    @patch('subprocess.check_call')
    @patch("tenx.util.verify_upload")
    def test_run_upload(self, verify_ul_patch, check_call_patch):
        check_call_patch.return_value = '0'
        verify_ul_patch.return_value = ""
        pwd = os.getcwd()

        asm = self.asm
        os.makedirs(asm.path)
        remote = self.remote_asm

        err = io.StringIO()
        sys.stderr = err
        with self.assertRaisesRegex(Exception, "Refusing to upload an unsuccessful assembly"):
            run_upload(asm, remote)

        outs_asm_d = asm.outs_assembly_path
        os.makedirs(outs_asm_d)

        err.seek(0, 0)
        run_upload(asm, remote)
        expected_err = "Upload TESTER assembly...\nLocal path: {0}\nEntering {0} ...\nUploading to: gs://data/TESTER/assembly\nRUNNING: gsutil -m rsync -r -x ASSEMBLER_CS/.*|outs/assembly/.* . gs://data/TESTER/assembly\nVerify upload assembly...\nUpload assembly...OK\n".format(asm.path)
        self.assertEqual(err.getvalue(), expected_err)
        sys.stderr = sys.__stderr__
        self.assertEqual(os.getcwd(), pwd)

# -- AsmUploadTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
