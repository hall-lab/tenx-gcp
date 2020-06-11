import io, os, subprocess, sys, tempfile, unittest
from mock import patch

from .context import tenx
from tenx.app import TenxApp
import tenx.assembly as assembly

class TenxAssemblyTest(unittest.TestCase):

    def setUp(self):
        self.temp_d = tempfile.TemporaryDirectory()
        os.chdir(self.temp_d.name)
        if TenxApp.config is None: TenxApp()
        TenxApp.config['TENX_DATA_PATH'] = self.temp_d.name
        TenxApp.config['TENX_REMOTE_URL'] = 'gs://data'
        TenxApp.config['TENX_ASM_CORES'] = "2"
        TenxApp.config['TENX_ASM_MEM'] = "2"

    def tearDown(self):
        self.temp_d.cleanup()
        TenxApp.config = None

    def test10_assembly(self):
        for base_path in TenxApp.config["TENX_DATA_PATH"], TenxApp.config["TENX_REMOTE_URL"]:
            asm = assembly.TenxAssembly(base_path=base_path, sample_name='TESTER')
            self.assertEqual(asm.base_path, os.path.join(base_path))
            self.assertEqual(asm.sample_name, "TESTER")
            self.assertEqual(asm.sample_path, os.path.join(base_path, 'TESTER'))
            self.assertEqual(asm.path, os.path.join(base_path, 'TESTER', 'assembly'))
            self.assertEqual(asm.reads_path, os.path.join(base_path, 'TESTER', 'reads'))
            self.assertEqual(asm.mkoutput_path, os.path.join(base_path, 'TESTER', 'assembly', 'mkoutput'))
            self.assertEqual(asm.outs_path, os.path.join(base_path, 'TESTER', 'assembly', 'outs'))
            self.assertEqual(asm.outs_assembly_path, os.path.join(base_path, 'TESTER', 'assembly', 'outs', 'assembly'))
            self.assertEqual(asm.outs_assembly_stats_path, os.path.join(base_path, 'TESTER', 'assembly', 'outs', 'assembly', 'stats'))

    def test11_is_successful(self):
        asm = assembly.TenxAssembly(sample_name='TESTER', base_path=TenxApp.config["TENX_DATA_PATH"])
        os.makedirs(asm.path)
        self.assertFalse(asm.is_successful())

        os.makedirs(os.path.join(asm.path, "outs", "assembly"))
        self.assertTrue(asm.is_successful())

    def test21_run_assemble_fails_without_supernova(self):
        err = io.StringIO()
        sys.stderr = err

        asm = assembly.TenxAssembly(sample_name='TESTER', base_path=TenxApp.config["TENX_DATA_PATH"])
        with self.assertRaisesRegex(Exception, "No such file or directory"):
            assembly.run_assemble(asm)
        self.assertFalse(os.path.exists(asm.sample_path))

        expected_err = "Checking if supernova is in PATH...\nRUNNING: supernova --help\n"
        self.assertEqual(err.getvalue(), expected_err)
        sys.stderr = sys.__stderr__

    @patch('subprocess.check_call')
    def test22_run_assemble_fails_when_no_outs_assembly_dir(self, check_call_patch):
        check_call_patch.return_value = '0'
        err = io.StringIO()
        sys.stderr = err

        asm = assembly.TenxAssembly(sample_name='TESTER', base_path=TenxApp.config["TENX_DATA_PATH"])
        with self.assertRaisesRegex(Exception, "Ran supernova script, but {} was not found".format(asm.outs_assembly_path)):
            assembly.run_assemble(asm)
        self.assertTrue(os.path.exists(asm.sample_path))

        expected_err = "Checking if supernova is in PATH...\nRUNNING: supernova --help\nRUNNING: supernova run --id=assembly --fastqs={} --uiport=18080 --nodebugmem --localcores=2 --localmem=2\n".format(asm.reads_path)
        self.assertEqual(err.getvalue(), expected_err)
        sys.stderr = sys.__stderr__

    @patch('subprocess.check_call')
    def test23_run_assemble_success(self, check_call_patch):
        check_call_patch.return_value = '0'
        err = io.StringIO()
        sys.stderr = err

        asm = assembly.TenxAssembly(sample_name='TESTER', base_path=TenxApp.config["TENX_DATA_PATH"])
        os.makedirs(asm.outs_assembly_path)
        assembly.run_assemble(asm)
        self.assertTrue(os.path.exists(asm.sample_path))

        expected_err = "Checking if supernova is in PATH...\nRUNNING: supernova --help\nRUNNING: supernova run --id=assembly --fastqs={} --uiport=18080 --nodebugmem --localcores=2 --localmem=2\n".format(asm.reads_path)
        self.assertEqual(err.getvalue(), expected_err)
        sys.stderr = sys.__stderr__

    @patch('subprocess.check_call')
    def test31_run_mkoutput_fails_with_incomplete_assembly(self, check_call_patch):
        check_call_patch.return_value = '0'
        err = io.StringIO()
        sys.stderr = err

        asm = assembly.TenxAssembly(sample_name='TESTER', base_path=TenxApp.config["TENX_DATA_PATH"])
        with self.assertRaisesRegex(Exception, "Assembly is not complete! Cannot run mkoutput!"):
            assembly.run_mkoutput(asm)
        expected_err = "Running mkoutput for TESTER...\n"
        self.assertEqual(err.getvalue(), expected_err)
        sys.stderr = sys.__stderr__

    @patch('subprocess.check_call')
    def test32_run_mkoutput_fails_without_all_fasta_files(self, check_call_patch):
        check_call_patch.return_value = '0'
        err = io.StringIO()
        sys.stderr = err

        asm = assembly.TenxAssembly(sample_name='TESTER', base_path=TenxApp.config["TENX_DATA_PATH"])
        outs_asm_d = asm.outs_assembly_path
        os.makedirs(outs_asm_d)
        with self.assertRaisesRegex(Exception, "Expected 4 assembly fasta.gz files in " + asm.mkoutput_path + " after running mkoutput, but found 0"):
            assembly.run_mkoutput(asm)
        expected_err = "Running mkoutput for TESTER...\nChecking if supernova is in PATH...\nRUNNING: supernova --help\nEntering {ASM_D}/mkoutput\nRUNNING: supernova mkoutput --asmdir={ASM_D}/outs/assembly --outprefix=TESTER.raw --style=raw\nRUNNING: supernova mkoutput --asmdir={ASM_D}/outs/assembly --outprefix=TESTER.megabubbles --style=megabubbles\nRUNNING: supernova mkoutput --asmdir={ASM_D}/outs/assembly --outprefix=TESTER.pseudohap2 --style=pseudohap2\n".format(ASM_D=asm.path)
        self.assertEqual(err.getvalue(), expected_err)
        sys.stderr = sys.__stderr__

    @patch('subprocess.check_call')
    def test33_run_mkoutput_success(self, check_call_patch):
        check_call_patch.return_value = '0'
        err = io.StringIO()
        sys.stderr = err

        asm = assembly.TenxAssembly(sample_name='TESTER', base_path=TenxApp.config["TENX_DATA_PATH"])
        outs_asm_d = asm.outs_assembly_path
        os.makedirs(outs_asm_d)
        mkoutput_d = asm.mkoutput_path
        os.makedirs(mkoutput_d)
        for n in range(4):
            with open(os.path.join(mkoutput_d, "{}.fasta.gz".format(n)), "w") as f:
                f.write(">SEQ1\nATGC")
                f.flush()
        assembly.run_mkoutput(asm)
        expected_err = "Running mkoutput for TESTER...\nChecking if supernova is in PATH...\nRUNNING: supernova --help\nEntering {ASM_D}/mkoutput\nRUNNING: supernova mkoutput --asmdir={ASM_D}/outs/assembly --outprefix=TESTER.raw --style=raw\nRUNNING: supernova mkoutput --asmdir={ASM_D}/outs/assembly --outprefix=TESTER.megabubbles --style=megabubbles\nRUNNING: supernova mkoutput --asmdir={ASM_D}/outs/assembly --outprefix=TESTER.pseudohap2 --style=pseudohap2\n".format(ASM_D=asm.path)
        self.assertEqual(err.getvalue(), expected_err)
        sys.stderr = sys.__stderr__

    @patch('subprocess.check_output')
    @patch('subprocess.check_call')
    @patch('subprocess.call')
    def test5_run_cleanup(self, call_patch, check_call_patch, check_output_patch):
        call_patch.return_value = 0
        check_call_patch.return_value = 0
        check_output_patch.return_value = b'0'
        pwd = os.getcwd()
        err = io.StringIO()
        sys.stderr = err
        with self.assertRaisesRegex(Exception, "Failed to find 4 mkoutput fasta files. Refusing to remove post assembly files"):
            asm = assembly.TenxAssembly(sample_name='TESTER', base_path=TenxApp.config["TENX_REMOTE_URL"])
            assembly.run_cleanup(asm)

        check_output_patch.return_value = b'a.fasta.gz\na.fasta.gz\na.fasta.gz\na.fasta.gz\n'
        err.seek(0, 0)
        asm = assembly.TenxAssembly(sample_name='TESTER', base_path=TenxApp.config["TENX_REMOTE_URL"])
        assembly.run_cleanup(asm)

        self.maxDiff = 10000
        expected_err = "Cleanup assembly for TESTER ...\nAssembly remote URL: gs://data/TESTER/assembly\nChecking if gsutil is installed...\nRUNNING: which gsutil\nChecking mkfastq files exist.\nRUNNING: gsutil ls gs://data/TESTER/assembly/mkoutput/*fasta.gz\nRemoving ASSEMBLER_CS logs path.\nRUNNING: gsutil -m rm -r gs://data/TESTER/assembly/ASSEMBLER_CS\nMoving outs / assembly / stats to outs.\nRUNNING: gsutil -m mv gs://data/TESTER/assembly/outs/assembly/stats gs://data/TESTER/assembly/outs\nRemoving outs / assembly path\nRUNNING: gsutil -m rm -r gs://data/TESTER/assembly/outs/assembly\nCleanup assembly ... OK\n"
        self.assertEqual(err.getvalue(), expected_err)
        self.assertEqual(os.getcwd(), pwd)

# -- TenxAssemblyTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__