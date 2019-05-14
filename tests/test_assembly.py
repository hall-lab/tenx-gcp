import os, subprocess, tempfile, unittest
from mock import patch

from .context import tenx
from tenx.app import TenxApp
from tenx import assembly

class TenxAppTest(unittest.TestCase):

    def test10_assembly(self):
        TenxApp()
        self.assertIsNotNone(TenxApp.config)
        TenxApp.config['TENX_DATA_PATH'] = '/tmp'
        TenxApp.config['TENX_REMOTE_URL'] = 'gs://data'
        asm = assembly.TenxAssembly(sample_name='TESTER')
        self.assertEqual(asm.sample_directory(), os.path.join(os.path.sep, TenxApp.config['TENX_DATA_PATH'], 'TESTER'))
        self.assertEqual(asm.local_directory(), os.path.join(os.path.sep, TenxApp.config['TENX_DATA_PATH'], 'TESTER', 'assembly'))
        self.assertEqual(asm.outs_assembly_directory(), os.path.join(os.path.sep, TenxApp.config['TENX_DATA_PATH'], 'TESTER', 'assembly', 'outs', 'assembly'))
        self.assertEqual(asm.reads_directory(), os.path.join(os.path.sep, TenxApp.config['TENX_DATA_PATH'], 'TESTER', 'reads'))
        self.assertEqual(asm.remote_url(), os.path.join(TenxApp.config['TENX_REMOTE_URL'], 'TESTER', 'assembly'))

    def test11_is_successful(self):
        TenxApp.config['TENX_DATA_PATH'] = os.path.join('tests', 'test_assembly')
        asm = assembly.TenxAssembly(sample_name='TEST_SUCCESS')
        self.assertTrue(asm.is_successful())
        asm = assembly.TenxAssembly(sample_name='TEST_FAIL')
        self.assertFalse(asm.is_successful())

    def test2_assemble_script(self):
        TenxApp.config['TENX_DATA_PATH'] = '/tmp'
        asm = assembly.TenxAssembly(sample_name='TESTER')
        with open(os.path.join('tests', 'test_assembly', 'scripts', 'assemble.sh'), 'r') as f:
            expected_script = f.read()
        script = assembly.assemble_script(asm)
        self.assertEqual(script, expected_script)

    @patch('subprocess.call')
    def test2_run_assemble(self, test_patch):
        test_patch.return_value = '0'
        TenxApp.config['TENX_DATA_PATH'] = os.path.join('tests', 'test_assembly')
        asm = assembly.TenxAssembly(sample_name='TEST_SUCCESS')
        assembly.run_assemble(asm)

        asm = assembly.TenxAssembly(sample_name='TEST_FAIL')
        with self.assertRaisesRegexp(Exception, "Ran supernova script, but " + asm.outs_assembly_directory() + " was not found"):
            assembly.run_assemble(asm)

    def test3_mkoutput_script(self):
        TenxApp.config['TENX_DATA_PATH'] = '/tmp'
        asm = assembly.TenxAssembly(sample_name='TESTER')
        with open(os.path.join('tests', 'test_assembly', 'scripts', 'mkoutput.sh'), 'r') as f:
            expected_script = f.read()
        script = assembly.mkoutput_script(asm)
        self.assertEqual(script, expected_script)

    @patch('subprocess.call')
    def test3_run_mkoutput(self, test_patch):
        test_patch.return_value = '0'
        TenxApp.config['TENX_DATA_PATH'] = os.path.join('tests', 'test_assembly')
        asm = assembly.TenxAssembly(sample_name='TEST_SUCCESS')
        assembly.run_mkoutput(asm)

        asm = assembly.TenxAssembly(sample_name='TEST_FAIL')
        with self.assertRaisesRegexp(Exception, "Expected 4 assembly fasta\.gz files in " + asm.mkoutput_directory() + " after running mkoutput, but only found 3"):
            assembly.run_mkoutput(asm)

    @patch('subprocess.call')
    def test4_run_upload(self, test_patch):
        # TODO test ASSEMBLER_CS dir is removed?
        test_patch.return_value = '0'
        TenxApp.config['TENX_DATA_PATH'] = os.path.join('tests', 'test_assembly')
        asm = assembly.TenxAssembly(sample_name='TEST_SUCCESS')
        assembly.run_upload(asm)

        asm = assembly.TenxAssembly(sample_name='TEST_FAIL')
        with self.assertRaisesRegexp(Exception, "Refusing to upload an unsuccessful assembly"):
            assembly.run_upload(asm)

# -- TenxAppTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
