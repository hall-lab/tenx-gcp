import io, os, subprocess, sys, tempfile, unittest
from mock import patch

from tenx.app import TenxApp
from tenx import reads
from tenx.sample import TenxSample

class TenxAppTest(unittest.TestCase):

    def setUp(self):
        self.temp_d = tempfile.TemporaryDirectory()
        if TenxApp.config is None: TenxApp()
        TenxApp.config['TENX_DATA_PATH'] = self.temp_d.name
        TenxApp.config['TENX_REMOTE_URL'] = 'gs://data'

    def tearDown(self):
        self.temp_d.cleanup()
        TenxApp.config = None

    @patch('subprocess.check_call')
    def test2_download_no_fastqs(self, test_patch):
        test_patch.return_value = 1
        lsample = TenxSample(base_path=TenxApp.config.get("TENX_DATA_PATH"), name='TESTER')
        rsample = TenxSample(base_path=TenxApp.config.get("TENX_REMOTE_URL"), name='TESTER')

        err = io.StringIO()
        sys.stderr = err

        with self.assertRaisesRegex(Exception, 'Failed to download read fastqs'):
            reads.download(lsample, rsample)
        self.assertTrue(os.path.exists(lsample.reads_path))

        expected_err = "Fetching {} fastqs from the object store...\nEntering {}\nChecking for sample reads at {} ...\n".format(rsample.name, lsample.reads_path, rsample.reads_path)
        self.assertEqual(err.getvalue(), expected_err)
        sys.stderr = sys.__stderr__

    @patch('subprocess.check_call')
    def test3_download(self, test_patch):
        test_patch.return_value = 1
        lsample = TenxSample(base_path=TenxApp.config.get("TENX_DATA_PATH"), name='TESTER')
        rsample = TenxSample(base_path=TenxApp.config.get("TENX_REMOTE_URL"), name='TESTER')
        os.makedirs(lsample.reads_path)
        with open(os.path.join(lsample.reads_path, 'read1.fastq'), 'w') as f:
            f.write("FASTQ\n") # a fastq file

        err = io.StringIO()
        sys.stderr = err

        reads.download(lsample, rsample)

        expected_err = "Fetching {} fastqs from the object store...\nEntering {}\nChecking for sample reads at {} ...\nFetching fastqs from the object store...OK\n".format(lsample.name, lsample.reads_path, rsample.reads_path)
        self.assertEqual(err.getvalue(), expected_err)
        sys.stderr = sys.__stderr__

# -- TenxAppTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
