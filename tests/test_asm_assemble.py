import io, os, subprocess, sys, tempfile, unittest
from mock import patch

from tenx.app import TenxApp
from tenx.assembly import run_assemble
from tenx.sample import TenxSample

class TenxAssemblyTest(unittest.TestCase):

    def setUp(self):
        self.temp_d = tempfile.TemporaryDirectory()
        os.chdir(self.temp_d.name)
        if TenxApp.config is None: TenxApp()
        TenxApp.config['TENX_DATA_PATH'] = self.temp_d.name
        TenxApp.config['TENX_ASM_CORES'] = "2"
        TenxApp.config['TENX_ASM_MEM'] = "2"

    def tearDown(self):
        self.temp_d.cleanup()
        TenxApp.config = None

    def test1_run_assemble_fails_without_supernova(self):
        err = io.StringIO()
        sys.stderr = err

        sample = TenxSample(name="TESTER", base_path=TenxApp.config.get("TENX_DATA_PATH"))
        asm = sample.assembly()
        with self.assertRaisesRegex(Exception, "No such file or directory"):
            run_assemble(asm)
        self.assertFalse(os.path.exists(sample.path))

        expected_err = "Checking if supernova is in PATH...\nRUNNING: supernova --help\n"
        self.assertEqual(err.getvalue(), expected_err)
        sys.stderr = sys.__stderr__

    @patch('subprocess.check_call')
    def test2_run_assemble_fails_when_no_outs_assembly_dir(self, check_call_patch):
        check_call_patch.return_value = '0'
        err = io.StringIO()
        sys.stderr = err

        sample = TenxSample(name="TESTER", base_path=TenxApp.config.get("TENX_DATA_PATH"))
        asm = sample.assembly()
        with self.assertRaisesRegex(Exception, "Ran supernova script, but {} was not found".format(asm.outs_assembly_path)):
            run_assemble(asm)
        self.assertTrue(os.path.exists(sample.path))

        expected_err = "Checking if supernova is in PATH...\nRUNNING: supernova --help\nRUNNING: supernova run --id=assembly --fastqs={} --maxreads=all --uiport=18080 --nodebugmem --localcores=2 --localmem=2\n".format(sample.reads_path)
        self.assertEqual(err.getvalue(), expected_err)
        sys.stderr = sys.__stderr__

    @patch('subprocess.check_call')
    def test3_run_assemble_success(self, check_call_patch):
        check_call_patch.return_value = '0'
        err = io.StringIO()
        sys.stderr = err

        sample = TenxSample(name="TESTER", base_path=TenxApp.config.get("TENX_DATA_PATH"))
        asm = sample.assembly()
        os.makedirs(asm.outs_assembly_path)
        run_assemble(asm)
        self.assertTrue(os.path.exists(sample.path))

        expected_err = "Checking if supernova is in PATH...\nRUNNING: supernova --help\nRUNNING: supernova run --id=assembly --fastqs={} --uiport=18080 --nodebugmem --localcores=2 --localmem=2\n".format(sample.reads_path)
        self.assertEqual(err.getvalue(), expected_err)
        sys.stderr = sys.__stderr__

# -- AsmAsembleTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
