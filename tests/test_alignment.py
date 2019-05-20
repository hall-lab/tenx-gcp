import os, subprocess, tempfile, unittest
from mock import patch

from .context import tenx
from tenx.app import TenxApp
from tenx import alignment

class TenxAlignmentTest(unittest.TestCase):

    def test10_alignment(self):
        TenxApp()
        self.assertIsNotNone(TenxApp.config)
        TenxApp.config['TENX_DATA_PATH'] = '/tmp'
        TenxApp.config['TENX_REMOTE_URL'] = 'gs://data'
        aln = alignment.TenxAlignment(sample_name='TESTER')
        self.assertEqual(aln.sample_directory(), os.path.join(os.path.sep, TenxApp.config['TENX_DATA_PATH'], 'TESTER'))
        self.assertEqual(aln.directory(), os.path.join(os.path.sep, TenxApp.config['TENX_DATA_PATH'], 'TESTER', 'alignment'))
        self.assertEqual(aln.outs_directory(), os.path.join(os.path.sep, TenxApp.config['TENX_DATA_PATH'], 'TESTER', 'alignment', 'outs'))
        self.assertEqual(aln.reads_directory(), os.path.join(os.path.sep, TenxApp.config['TENX_DATA_PATH'], 'TESTER', 'reads'))
        self.assertEqual(aln.remote_url(), os.path.join(TenxApp.config['TENX_REMOTE_URL'], 'TESTER', 'alignment'))

    def test11_is_successful(self):
        TenxApp.config['TENX_DATA_PATH'] = os.path.join('tests', 'test_alignment')
        aln = alignment.TenxAlignment(sample_name='TEST_SUCCESS')
        self.assertTrue(aln.is_successful())
        aln = alignment.TenxAlignment(sample_name='TEST_FAIL')
        self.assertFalse(aln.is_successful())

# -- TenxAlignmentTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
