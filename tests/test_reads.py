import os, subprocess, tempfile, unittest
from mock import patch

from .context import tenx
from tenx.app import TenxApp
from tenx import reads

class TenxAppTest(unittest.TestCase):

    def test1_reads(self):
        tenxapp = TenxApp()
        self.assertIsNotNone(TenxApp.config)
        TenxApp.config['TENX_DATA_PATH'] = tempfile.mkdtemp()
        TenxApp.config['TENX_REMOTE_URL'] = 'gs://data'
        r = reads.TenxReads(sample_name='TESTER')
        self.assertEqual(r.local_directory(), os.path.join(os.path.sep, TenxApp.config['TENX_DATA_PATH'], 'TESTER', 'reads'))
        self.assertEqual(r.remote_url(), os.path.join(TenxApp.config['TENX_REMOTE_URL'], 'TESTER', 'reads'))

    @patch('subprocess.check_call')
    def test2_download_no_fastqs(self, test_patch):
        test_patch.return_value = 1
        r = reads.TenxReads(sample_name='TESTER')
        self.assertIsNotNone(r)
        #with self.assertRaisesRegexp(subprocess.CalledProcessError, 'BucketNotFoundException'):
        #    reads.download(r)
        with self.assertRaisesRegexp(Exception, 'Failed to download read fastqs'):
            reads.download(r)
        self.assertTrue(os.path.exists(r.local_directory()))

    @patch('subprocess.check_call')
    def test3_download(self, test_patch):
        test_patch.return_value = 1
        r = reads.TenxReads(sample_name='TESTER')
        self.assertIsNotNone(r)
        with open(os.path.join(r.local_directory(), 'read1.fastq'), 'w') as f: f.write("FASTQ\n") # a fastq file
        reads.download(r)

# -- TenxAppTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
