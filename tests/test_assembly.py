import os, subprocess, tempfile, unittest
from mock import patch

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

    def test2_mkoutput_script(self):
        asm = assembly.TenxAssembly(sample_name='TESTER')
        with open(os.path.join('tests', 'test_assembly', 'mkoutput', 'mkoutput.sh'), 'r') as f:
            expected_script = f.read()
        script = assembly.mkoutput_script(asm)
        self.assertEqual(script, expected_script)

    @patch('subprocess.call')
    def test2_run_mkoutput(self, test_patch):
        test_patch.return_value = '0'
        TenxApp.config['TENX_DATA_PATH'] = os.path.join('tests', 'test_assembly', 'mkoutput')
        asm = assembly.TenxAssembly(sample_name='TEST_SUCCESS')
        assembly.run_mkoutput(asm)

        asm = assembly.TenxAssembly(sample_name='TEST_FAIL')
        with self.assertRaisesRegexp(Exception, "Expected 4 assembly fasta\.gz files in " + asm.mkoutput_directory() + " after running mkoutput, but only found 3"):
            assembly.run_mkoutput(asm)

# -- TenxAppTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
