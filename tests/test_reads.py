import io, os, shutil, subprocess, sys, tempfile, unittest
from mock import patch

from .context import tenx
from tenx.app import TenxApp
from tenx import reads

class TenxAppTest(unittest.TestCase):

    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
        if TenxApp.config is None: TenxApp()
        TenxApp.config['TENX_DATA_PATH'] = self.tempdir
        TenxApp.config['TENX_REMOTE_URL'] = 'gs://data'

    def tearDown(self):
        shutil.rmtree(self.tempdir)
        TenxApp.config = None

    def test1_reads(self):
        r = reads.TenxReads(sample_name='TESTER')
        self.assertEqual(r.directory(), os.path.join(os.path.sep, TenxApp.config['TENX_DATA_PATH'], 'TESTER', 'reads'))
        self.assertEqual(r.remote_url(), os.path.join(TenxApp.config['TENX_REMOTE_URL'], 'TESTER', 'reads'))

    @patch('subprocess.check_call')
    def test2_download_no_fastqs(self, test_patch):
        test_patch.return_value = 1
        r = reads.TenxReads(sample_name='TESTER')
        self.assertIsNotNone(r)

        err = io.StringIO()
        sys.stderr = err

        with self.assertRaisesRegex(Exception, 'Failed to download read fastqs'):
            reads.download(r)
        self.assertTrue(os.path.exists(r.directory()))

        expected_err = "Fetching {} fastqs from the object store...\nEntering {}\nChecking for sample reads at {} ...\n".format(r.sample_name, r.directory(), r.remote_url())
        self.assertEqual(err.getvalue(), expected_err)
        sys.stderr = sys.__stderr__

    @patch('subprocess.check_call')
    def test3_download(self, test_patch):
        test_patch.return_value = 1
        r = reads.TenxReads(sample_name='TESTER')
        self.assertIsNotNone(r)
        os.makedirs(r.directory())
        with open(os.path.join(r.directory(), 'read1.fastq'), 'w') as f: f.write("FASTQ\n") # a fastq file

        err = io.StringIO()
        sys.stderr = err

        reads.download(r)

        expected_err = "Fetching {} fastqs from the object store...\nEntering {}\nChecking for sample reads at {} ...\nFetching fastqs from the object store...OK\n".format(r.sample_name, r.directory(), r.remote_url())
        self.assertEqual(err.getvalue(), expected_err)
        sys.stderr = sys.__stderr__

# -- TenxAppTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
