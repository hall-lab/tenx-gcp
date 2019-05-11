import os, tempfile, unittest

from .context import tenx
from tenx.app import TenxApp
from tenx import assembly

class TenxAppTest(unittest.TestCase):

    def test1_assembly(self):
        TenxApp()
        self.assertIsNotNone(TenxApp.config)
        TenxApp.config['TENX_DATA_PATH'] = '/tmp'
        TenxApp.config['TENX_REMOTE_URL'] = 'gs://data'
        asm = assembly.TenxAssembly(sample_name='TESTER')
        self.assertEqual(asm.local_directory(), os.path.join(os.path.sep, TenxApp.config['TENX_DATA_PATH'], 'TESTER', 'assembly'))
        self.assertEqual(asm.remote_url(), os.path.join(TenxApp.config['TENX_REMOTE_URL'], 'TESTER', 'assembly'))

    def test2_mkoutput(self):
        asm = assembly.TenxAssembly(sample_name='TESTER')
        with open(os.path.join('tests', 'test_assembly', 'mkoutput.sh'), 'r') as f:
            expected_script = f.read()
        script = assembly.mkoutput_script(asm)
        self.assertEqual(script, expected_script)    

# -- TenxAppTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
