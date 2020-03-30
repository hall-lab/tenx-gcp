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
        asm = assembly.TenxAssembly(sample_name='TESTER')
        self.assertEqual(asm.sample_directory(), os.path.join(os.path.sep, TenxApp.config['TENX_DATA_PATH'], 'TESTER'))
        self.assertEqual(asm.directory(), os.path.join(os.path.sep, TenxApp.config['TENX_DATA_PATH'], 'TESTER', 'assembly'))
        self.assertEqual(asm.reads_directory(), os.path.join(os.path.sep, TenxApp.config['TENX_DATA_PATH'], 'TESTER', 'reads'))
        self.assertEqual(asm.mkoutput_path(), os.path.join(os.path.sep, TenxApp.config['TENX_DATA_PATH'], 'TESTER', 'assembly', 'mkoutput'))
        self.assertEqual(asm.outs_path(), os.path.join(os.path.sep, TenxApp.config['TENX_DATA_PATH'], 'TESTER', 'assembly', 'outs'))
        self.assertEqual(asm.outs_assembly_path(), os.path.join(os.path.sep, TenxApp.config['TENX_DATA_PATH'], 'TESTER', 'assembly', 'outs', 'assembly'))
        self.assertEqual(asm.outs_assembly_stats_path(), os.path.join(os.path.sep, TenxApp.config['TENX_DATA_PATH'], 'TESTER', 'assembly', 'outs', 'assembly', 'stats'))

        self.assertEqual(asm.remote_url, os.path.join(TenxApp.config['TENX_REMOTE_URL'], 'TESTER', 'assembly'))
        self.assertEqual(asm.mkoutput_path(remote=True), os.path.join(TenxApp.config['TENX_REMOTE_URL'], 'TESTER', 'assembly', 'mkoutput'))
        self.assertEqual(asm.outs_path(remote=True), os.path.join(TenxApp.config['TENX_REMOTE_URL'], 'TESTER', 'assembly', 'outs'))
        self.assertEqual(asm.outs_assembly_path(remote=True), os.path.join(TenxApp.config['TENX_REMOTE_URL'], 'TESTER', 'assembly', 'outs', 'assembly'))
        self.assertEqual(asm.outs_assembly_stats_path(remote=True), os.path.join(TenxApp.config['TENX_REMOTE_URL'], 'TESTER', 'assembly', 'outs', 'assembly', 'stats'))

    def test11_is_successful(self):
        asm = assembly.TenxAssembly(sample_name='TESTER')
        os.makedirs(asm.directory())
        self.assertFalse(asm.is_successful())

        os.makedirs(os.path.join(asm.directory(), "outs", "assembly"))
        self.assertTrue(asm.is_successful())

    def test21_run_assemble_fails_without_supernova(self):
        err = io.StringIO()
        sys.stderr = err

        asm = assembly.TenxAssembly(sample_name='TESTER')
        with self.assertRaisesRegex(Exception, "No such file or directory"):
            assembly.run_assemble(asm)
        self.assertFalse(os.path.exists(asm.sample_directory()))

        expected_err = "Checking if supernova is in PATH...\nRUNNING: supernova --help\n"
        self.assertEqual(err.getvalue(), expected_err)
        sys.stderr = sys.__stderr__

    @patch('subprocess.check_call')
    def test22_run_assemble_fails_when_no_outs_assembly_dir(self, check_call_patch):
        check_call_patch.return_value = '0'
        err = io.StringIO()
        sys.stderr = err

        asm = assembly.TenxAssembly(sample_name='TESTER')
        with self.assertRaisesRegex(Exception, "Ran supernova script, but {} was not found".format(asm.outs_assembly_path())):
            assembly.run_assemble(asm)
        self.assertTrue(os.path.exists(asm.sample_directory()))

        expected_err = "Checking if supernova is in PATH...\nRUNNING: supernova --help\nRUNNING: supernova run --id=assembly --fastqs={} --uiport=18080 --nodebugmem --localcores=2 --localmem=2\n".format(asm.reads_directory())
        self.assertEqual(err.getvalue(), expected_err)
        sys.stderr = sys.__stderr__

    @patch('subprocess.check_call')
    def test23_run_assemble_success(self, check_call_patch):
        check_call_patch.return_value = '0'
        err = io.StringIO()
        sys.stderr = err

        asm = assembly.TenxAssembly(sample_name='TESTER')
        os.makedirs(asm.outs_assembly_path())
        assembly.run_assemble(asm)
        self.assertTrue(os.path.exists(asm.sample_directory()))

        expected_err = "Checking if supernova is in PATH...\nRUNNING: supernova --help\nRUNNING: supernova run --id=assembly --fastqs={} --uiport=18080 --nodebugmem --localcores=2 --localmem=2\n".format(asm.reads_directory())
        self.assertEqual(err.getvalue(), expected_err)
        sys.stderr = sys.__stderr__

    @patch('subprocess.check_call')
    def test31_run_mkoutput_fails_with_incomplete_assembly(self, check_call_patch):
        check_call_patch.return_value = '0'
        err = io.StringIO()
        sys.stderr = err

        asm = assembly.TenxAssembly(sample_name='TESTER')
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

        asm = assembly.TenxAssembly(sample_name='TESTER')
        outs_asm_d = asm.outs_assembly_path()
        os.makedirs(outs_asm_d)
        with self.assertRaisesRegex(Exception, "Expected 4 assembly fasta.gz files in " + asm.mkoutput_path() + " after running mkoutput, but found 0"):
            assembly.run_mkoutput(asm)
        expected_err = "Running mkoutput for TESTER...\nChecking if supernova is in PATH...\nRUNNING: supernova --help\nEntering {ASM_D}/mkoutput\nRUNNING: supernova mkoutput --asmdir={ASM_D}/outs/assembly --outprefix=TESTER.raw --style=raw\nRUNNING: supernova mkoutput --asmdir={ASM_D}/outs/assembly --outprefix=TESTER.megabubbles --style=megabubbles\nRUNNING: supernova mkoutput --asmdir={ASM_D}/outs/assembly --outprefix=TESTER.pseudohap2 --style=pseudohap2\n".format(ASM_D=asm.directory())
        self.assertEqual(err.getvalue(), expected_err)
        sys.stderr = sys.__stderr__

    @patch('subprocess.check_call')
    def test33_run_mkoutput_success(self, check_call_patch):
        check_call_patch.return_value = '0'
        err = io.StringIO()
        sys.stderr = err

        asm = assembly.TenxAssembly(sample_name='TESTER')
        outs_asm_d = asm.outs_assembly_path()
        os.makedirs(outs_asm_d)
        mkoutput_d = asm.mkoutput_path()
        os.makedirs(mkoutput_d)
        for n in range(4):
            with open(os.path.join(mkoutput_d, "{}.fasta.gz".format(n)), "w") as f:
                f.write(">SEQ1\nATGC")
                f.flush()
        assembly.run_mkoutput(asm)
        expected_err = "Running mkoutput for TESTER...\nChecking if supernova is in PATH...\nRUNNING: supernova --help\nEntering {ASM_D}/mkoutput\nRUNNING: supernova mkoutput --asmdir={ASM_D}/outs/assembly --outprefix=TESTER.raw --style=raw\nRUNNING: supernova mkoutput --asmdir={ASM_D}/outs/assembly --outprefix=TESTER.megabubbles --style=megabubbles\nRUNNING: supernova mkoutput --asmdir={ASM_D}/outs/assembly --outprefix=TESTER.pseudohap2 --style=pseudohap2\n".format(ASM_D=asm.directory())
        self.assertEqual(err.getvalue(), expected_err)
        sys.stderr = sys.__stderr__

    @patch('subprocess.check_call')
    @patch("tenx.util.verify_upload")
    def test4_run_upload(self, verify_ul_patch, check_call_patch):
        check_call_patch.return_value = '0'
        verify_ul_patch.return_value = ""
        pwd = os.getcwd()

        asm = assembly.TenxAssembly(sample_name='TESTER')
        os.makedirs(asm.directory())

        err = io.StringIO()
        sys.stderr = err
        with self.assertRaisesRegex(Exception, "Refusing to upload an unsuccessful assembly"):
            assembly.run_upload(asm)

        outs_asm_d = asm.outs_assembly_path()
        os.makedirs(outs_asm_d)

        err.seek(0, 0)
        assembly.run_upload(asm)

        expected_err = "Upload TESTER assembly...\nLocal path: {0}\nEntering {0} ...\nUploading to: gs://data/TESTER/assembly\nRUNNING: gsutil -m rsync -r -x ASSEMBLER_CS/.*|outs/assembly/.* . gs://data/TESTER/assembly\nVerify upload assembly...\nUpload assembly...OK\n".format(asm.directory())
        self.assertEqual(err.getvalue(), expected_err)
        sys.stderr = sys.__stderr__
        self.assertEqual(os.getcwd(), pwd)

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
            asm = assembly.TenxAssembly(sample_name='TESTER')
            assembly.run_cleanup(asm)

        check_output_patch.return_value = b'a.fasta.gz\na.fasta.gz\na.fasta.gz\na.fasta.gz\n'
        err.seek(0, 0)
        asm = assembly.TenxAssembly(sample_name='TESTER')
        assembly.run_cleanup(asm)

        self.maxDiff = 10000
        expected_err = "Cleanup assembly for TESTER ...\nAssembly remote URL: gs://data/TESTER/assembly\nChecking if gsutil is installed...\nRUNNING: which gsutil\nAssembly is incorrect path, will move after cleanup.\nChecking mkfastq files exist.\nRUNNING: gsutil ls gs://data/TESTER/assembly/TESTER/mkoutput/*fasta.gz\nRemoving ASSEMBLER_CS logs path.\nRUNNING: gsutil -m rm -r gs://data/TESTER/assembly/TESTER/ASSEMBLER_CS\nMoving outs / assembly / stats to outs.\nRUNNING: gsutil -m mv gs://data/TESTER/assembly/TESTER/outs/assembly/stats gs://data/TESTER/assembly/TESTER/outs\nRemoving outs / assembly path\nRUNNING: gsutil -m rm -r gs://data/TESTER/assembly/TESTER/outs/assembly\nMoving assembly to correct path...\nCleanup assembly ... OK\n"
        self.assertEqual(err.getvalue(), expected_err)
        self.assertEqual(os.getcwd(), pwd)

# -- TenxAssemblyTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
