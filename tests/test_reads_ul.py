import io, os, subprocess, sys, tempfile, unittest
from click.testing import CliRunner
from mock import patch

from tenx.app import TenxApp
import tenx.reads_ul
from tenx.sample import TenxSample

class TenxAppTest(unittest.TestCase):

    def setUp(self):
        self.temp_d = tempfile.TemporaryDirectory()
        if TenxApp.config is None: TenxApp()
        TenxApp.config['TENX_DATA_PATH'] = self.temp_d.name
        TenxApp.config['TENX_REMOTE_URL'] = 'gs://data'

        self.lsample = TenxSample(base_path=TenxApp.config.get("TENX_DATA_PATH"), name='TEST-001')
        os.makedirs(self.lsample.reads_path)
        with open(os.path.join(self.lsample.reads_path, 'read1.fastq'), 'w') as f:
            f.write("FASTQ\n") # a fastq file
        self.rsample = TenxSample(base_path=TenxApp.config.get("TENX_REMOTE_URL"), name='TEST-001')

    def tearDown(self):
        self.temp_d.cleanup()
        TenxApp.config = None
        sys.stderr = sys.__stderr__

    @patch('subprocess.check_call')
    def test_ul_no_fastqs(self, check_call_p):
        check_call_p.return_value = 1
        err = io.StringIO()
        sys.stderr = err

        blah_dn = os.path.join(self.temp_d.name, "blah")
        lsample = TenxSample(base_path=blah_dn, name=self.lsample.name)
        with self.assertRaisesRegex(Exception, 'Sample reads path does not exist!'):
            tenx.reads_ul.ul(lsample, self.rsample)

        os.makedirs(lsample.reads_path)
        with self.assertRaisesRegex(Exception, "Did find any fastqs in reads path!"):
            tenx.reads_ul.ul(lsample, self.rsample)

        #FIXME
        #expected_err = "Upload {} reads fastqs to the object store via sync...\nChecking for fastqs in {}\n".format(lsample.name, lsample.reads_path)
        #self.assertEqual(err.getvalue(), expected_err)
        #check_call_p.called_once_with([])

    @patch('subprocess.check_call')
    def test_ul(self, check_call_p):
        check_call_p.return_value = 1
        err = io.StringIO()
        sys.stderr = err

        tenx.reads_ul.ul(self.lsample, self.rsample)

        expected_err = "Upload {} reads fastqs to the object store via sync...\nChecking for fastqs in {}\nFound 1 fastq(s)\nUpload to {}\nDone\n".format(self.lsample.name, self.lsample.reads_path, self.rsample.reads_path)
        self.assertEqual(err.getvalue(), expected_err)

    @patch('tenx.reads_ul.ul')
    def test_ul_cmd(self, ul_p):
        ul_p.return_value = 1
        runner = CliRunner()
        result = runner.invoke(tenx.reads_ul.ul_cmd, ["--help"])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(tenx.reads_ul.ul_cmd, [])
        self.assertEqual(result.exit_code, 2)

        result = runner.invoke(tenx.reads_ul.ul_cmd, [self.lsample.name])
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise

        expected_output = ""
        self.assertEqual(result.output, expected_output)

# -- TenxAppTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
