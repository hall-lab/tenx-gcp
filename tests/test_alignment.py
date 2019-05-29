import os, subprocess, tempfile, unittest
from mock import patch

from .context import tenx
from tenx.app import TenxApp
from tenx import alignment, reads, reference
from tenx.alignment import TenxAlignment
from tenx.reads import TenxReads
from tenx.reference import TenxReference

class TenxAlignmentTest(unittest.TestCase):

    def test10_alignment(self):
        TenxApp()
        self.assertIsNotNone(TenxApp.config)
        TenxApp.config['TENX_DATA_PATH'] = '/tmp'
        TenxApp.config['TENX_REMOTE_URL'] = 'gs://data'
        aln = TenxAlignment(sample_name='TESTER')
        self.assertEqual(aln.sample_directory(), os.path.join(os.path.sep, TenxApp.config['TENX_DATA_PATH'], 'TESTER'))
        self.assertEqual(aln.directory(), os.path.join(os.path.sep, TenxApp.config['TENX_DATA_PATH'], 'TESTER', 'alignment'))
        self.assertEqual(aln.outs_directory(), os.path.join(os.path.sep, TenxApp.config['TENX_DATA_PATH'], 'TESTER', 'alignment', 'outs'))
        self.assertEqual(aln.remote_url(), os.path.join(TenxApp.config['TENX_REMOTE_URL'], 'TESTER', 'alignment'))

    def test11_is_successful(self):
        TenxApp.config['TENX_DATA_PATH'] = os.path.join('tests', 'test_alignment')
        aln = TenxAlignment(sample_name='TEST_SUCCESS')
        self.assertTrue(aln.is_successful())
        aln = TenxAlignment(sample_name='TEST_FAIL')
        self.assertFalse(aln.is_successful())

    @patch('subprocess.check_call')
    def test2_run_align(self, test_patch):
        test_patch.return_value = '0'
        TenxApp.config['TENX_DATA_PATH'] = os.path.join(os.getcwd(), 'tests', 'test_alignment')
        aln = TenxAlignment(sample_name='TEST_SUCCESS')
        alignment.run_align(aln, TenxReference(name="REF"), TenxReads(sample_name="TEST_SUCCESS"))

        aln = TenxAlignment(sample_name='TEST_FAIL')
        with self.assertRaisesRegexp(Exception, "Longranger exited 0, but {} does not exist!".format(aln.outs_directory())):
            alignment.run_align(aln, TenxReference(name="REF"), TenxReads(sample_name="TEST_SUCCESS"))

    @patch('subprocess.check_call')
    def test4_run_upload(self, test_patch):
        test_patch.return_value = '0'
        TenxApp.config['TENX_DATA_PATH'] = os.path.join('tests', 'test_alignment')
        aln = TenxAlignment(sample_name='TEST_SUCCESS')
        alignment.run_upload(aln)

        aln = TenxAlignment(sample_name='TEST_FAIL')
        with self.assertRaisesRegexp(Exception, "Refusing to upload an unsuccessful alignment"):
            alignment.run_upload(aln)

# -- TenxAlignmentTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
