import os, sys, unittest

from .context import tenx
from tenx.app import TenxApp
from tenx import reads

class TenxAppTest(unittest.TestCase):

    def test1_reads(self):
        tenxapp = TenxApp()
        self.assertIsNotNone(TenxApp.config)
        TenxApp.config['TENX_DATA_PATH'] = '/tmp'
        TenxApp.config['TENX_REMOTE_URL'] = '/tmp'
        r = reads.TenxReads(sample_name='TESTER')
        self.assertEqual(r.local_directory(), os.path.join(os.path.sep, 'tmp', 'TESTER', 'reads'))
        self.assertEqual(r.remote_url(), os.path.join(os.path.sep, 'tmp', 'TESTER', 'reads'))

    def test2_download(self):
        pass

# -- TenxAppTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
