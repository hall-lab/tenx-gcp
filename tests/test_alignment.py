import io, os, shutil, subprocess, sys, tempfile, unittest
from mock import patch

from .context import tenx
from tenx.app import TenxApp
from tenx import alignment, reads, reference
from tenx.alignment import TenxAlignment
from tenx.reference import TenxReference

class TenxAlignmentTest(unittest.TestCase):

    def setUp(self):
        self.temp_d = tempfile.TemporaryDirectory()
        if TenxApp.config is None: TenxApp()
        TenxApp.config['TENX_DATA_PATH'] = self.temp_d.name
        TenxApp.config['TENX_REMOTE_URL'] = 'gs://data'
        TenxApp.config['TENX_REMOTE_REFS_URL'] = 'gs://data/references'
        TenxApp.config['TENX_ALN_MODE'] = 'local'
        TenxApp.config['TENX_ALN_CORES'] = '1'
        TenxApp.config['TENX_ALN_MEM'] = '6'
        TenxApp.config['TENX_ALN_VCMODE'] = 'freebayes'
 
    def tearDown(self):
        self.temp_d.cleanup()
        TenxApp.config = None

    def test10_alignment(self):
        aln = TenxAlignment(sample_name='TESTER')
        self.assertEqual(aln.sample.path, os.path.join(os.path.sep, TenxApp.config['TENX_DATA_PATH'], 'TESTER'))
        self.assertEqual(aln.directory(), os.path.join(os.path.sep, TenxApp.config['TENX_DATA_PATH'], 'TESTER', 'alignment'))
        self.assertEqual(aln.outs_directory(), os.path.join(os.path.sep, TenxApp.config['TENX_DATA_PATH'], 'TESTER', 'alignment', 'outs'))
        self.assertEqual(aln.remote_url(), os.path.join(TenxApp.config['TENX_REMOTE_URL'], 'TESTER', 'alignment'))

    def test11_is_successful(self):
        aln = TenxAlignment(sample_name='TEST_SUCCESS')
        os.makedirs( os.path.join(aln.directory(), "outs") )
        with open(os.path.join(aln.directory(), "outs", "summary.csv"), "w") as f: f.write("SUCCESS!")
        self.assertTrue(aln.is_successful())

        aln = TenxAlignment(sample_name='TEST_FAIL')
        os.makedirs(aln.directory())
        self.assertFalse(aln.is_successful())

    @patch('subprocess.check_call')
    def test2_run_align(self, test_patch):
        test_patch.return_value = '0'
        err = io.StringIO()
        sys.stderr = err

        aln = TenxAlignment(sample_name='TEST_SUCCESS')
        os.makedirs( os.path.join(aln.directory(), "outs") )
        with open(os.path.join(aln.directory(), "outs", "summary.csv"), "w") as f: f.write("SUCCESS!")
        ref = TenxReference(name="REF")
        alignment.run_align(aln, ref)

        expected_err = "Creating alignments for TEST_SUCCESS\nEntering {}\nRunning longranger wgs --id=alignment --sample=TEST_SUCCESS --reference={} --fastqs={} --vcmode=freebayes --disable-ui --jobmode=local --localmem=6 --localcores=1 ...\n".format(aln.sample.path, ref.directory(), aln.sample.reads_path)
        self.assertEqual(err.getvalue(), expected_err)
        sys.stderr = sys.__stderr__

    @patch('subprocess.check_call')
    @patch('tenx.util.verify_upload')
    def test4_run_upload(self, upload_patch, verify_patch):
        sys.stderr = io.StringIO()
        aln = TenxAlignment(sample_name='TEST_FAIL')
        os.makedirs( os.path.join(aln.directory(), "outs") )
        with self.assertRaisesRegex(Exception, "Refusing to upload an unsuccessful alignment"):
            alignment.run_upload(aln)

        upload_patch.return_value = "0"
        verify_patch.return_value = "1"

        aln = TenxAlignment(sample_name='TEST_SUCCESS')
        os.makedirs( os.path.join(aln.directory(), "outs") )
        with open(os.path.join(aln.directory(), "outs", "summary.csv"), "w") as f: f.write("SUCCESS!")

        err = io.StringIO()
        sys.stderr = err

        alignment.run_upload(aln)

        expected_err = "Upload TEST_SUCCESS alignment...\nEntering {} ...\nUploading to: {}\nVerify upload alignment...\nUpload alignment...OK\n".format(aln.directory(), aln.remote_url())
        self.assertEqual(err.getvalue(), expected_err)
        sys.stderr = sys.__stderr__

# -- TenxAlignmentTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
