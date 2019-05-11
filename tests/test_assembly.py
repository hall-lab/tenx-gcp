import os, tempfile, unittest

from .context import tenx
from tenx.app import TenxApp
from tenx import assembly

class TenxAppTest(unittest.TestCase):

    def test1_assembly(self):
        TenxApp()
        self.assertIsNotNone(TenxApp.config)
        TenxApp.config['TENX_DATA_PATH'] = tempfile.mkdtemp()
        TenxApp.config['TENX_REMOTE_URL'] = 'gs://data'
        r = assembly.TenxAssembly(sample_name='TESTER')
        self.assertEqual(r.local_directory(), os.path.join(os.path.sep, TenxApp.config['TENX_DATA_PATH'], 'TESTER', 'assembly'))
        self.assertEqual(r.remote_url(), os.path.join(TenxApp.config['TENX_REMOTE_URL'], 'TESTER', 'assembly'))

# -- TenxAppTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
