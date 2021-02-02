import io, os, shutil, subprocess, sys, tempfile, unittest
from mock import patch

from tenx.app import TenxApp
from tenx import alignment, reads, reference
from tenx.alignment import TenxAlignment
from tenx.reference import TenxReference
from tenx.sample import TenxSample

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
        sample = TenxSample(name="TESTER", base_path=TenxApp.config['TENX_DATA_PATH'])
        aln = sample.alignment()
        self.assertEqual(os.path.join(sample.path, "alignment"), aln.path)
        self.assertEqual(os.path.join(aln.path, 'outs'), aln.outs_path)

    def test11_is_successful(self):
        sample = TenxSample(name="TEST_SUCCESS", base_path=TenxApp.config['TENX_DATA_PATH'])
        aln = sample.alignment()
        os.makedirs( os.path.join(aln.outs_path) )
        with open(os.path.join(aln.outs_path, "summary.csv"), "w") as f: f.write("SUCCESS!")
        self.assertTrue(aln.is_successful())

        sample = TenxSample(name="TEST_FAIL", base_path=TenxApp.config['TENX_DATA_PATH'])
        aln = sample.alignment()
        os.makedirs(aln.path)
        self.assertFalse(aln.is_successful())

    @patch('subprocess.check_call')
    def test2_run_align(self, test_patch):
        test_patch.return_value = '0'
        err = io.StringIO()
        sys.stderr = err

        sample = TenxSample(name="TEST_SUCCESS", base_path=TenxApp.config['TENX_DATA_PATH'])
        aln = sample.alignment()
        os.makedirs( os.path.join(aln.path, "outs") )
        with open(os.path.join(aln.path, "outs", "summary.csv"), "w") as f: f.write("SUCCESS!")
        ref = TenxReference(name="REF")
        alignment.run_align(aln, ref)

        expected_err = "Creating alignments for TEST_SUCCESS\nEntering {}\nRunning longranger wgs --id=alignment --sample=TEST_SUCCESS --reference={} --fastqs={} --vcmode=freebayes --disable-ui --jobmode=local --localmem=6 --localcores=1 ...\n".format(aln.sample.path, ref.directory(), aln.sample.reads_path)
        self.assertEqual(err.getvalue(), expected_err)
        sys.stderr = sys.__stderr__

    @patch('subprocess.check_call')
    @patch('tenx.util.verify_upload')
    def test4_run_upload(self, upload_patch, verify_patch):
        sys.stderr = io.StringIO()
        sample = TenxSample(name='TEST_FAIL', base_path=TenxApp.config['TENX_DATA_PATH'])
        aln = sample.alignment()
        rsample = TenxSample(name='TEST_FAIL', base_path=TenxApp.config['TENX_REMOTE_URL'])
        raln = rsample.alignment()
        os.makedirs( os.path.join(aln.outs_path) )
        with self.assertRaisesRegex(Exception, "Refusing to upload an unsuccessful alignment"):
            alignment.run_upload(aln, raln)

        upload_patch.return_value = "0"
        verify_patch.return_value = "1"

        sample = TenxSample(name='TEST_SUCCESS', base_path=TenxApp.config['TENX_DATA_PATH'])
        aln = sample.alignment()
        os.makedirs( os.path.join(aln.path, "outs") )
        with open(os.path.join(aln.path, "outs", "summary.csv"), "w") as f: f.write("SUCCESS!")
        rsample = TenxSample(name='TEST_SUCCESS', base_path=TenxApp.config['TENX_DATA_PATH'])
        raln = rsample.alignment()

        err = io.StringIO()
        sys.stderr = err

        alignment.run_upload(aln, raln)
        expected_err = "Upload TEST_SUCCESS alignment...\nEntering {} ...\nUploading to: {}\nVerify upload alignment...\nUpload alignment...OK\n".format(aln.path, raln.path)
        self.assertEqual(err.getvalue(), expected_err)
        sys.stderr = sys.__stderr__

# -- TenxAlignmentTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
