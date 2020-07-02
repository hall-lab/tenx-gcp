import gzip, io, os, shutil, subprocess, sys, tarfile, tempfile, unittest
from mock import patch

from tenx.app import TenxApp
from tenx import reference

class TenxAppTest(unittest.TestCase):

    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
        os.chdir(self.tempdir)
        if TenxApp.config is None: TenxApp()
        TenxApp.config['TENX_DATA_PATH'] = self.tempdir
        TenxApp.config['TENX_REMOTE_REFS_URL'] = 'gs://data/references'

    def tearDown(self):
        shutil.rmtree(self.tempdir)
        TenxApp.config = None

    def test1_reference(self):
        r = reference.TenxReference(name='refdata-GRCh38-2.1.0')
        self.assertEqual(r.references_directory(), os.path.join(os.path.sep, TenxApp.config['TENX_DATA_PATH'], 'references'))
        self.assertEqual(r.directory(), os.path.join(r.references_directory(), r.name))
        self.assertEqual(r.genome_fasta_fn(), os.path.join(r.directory(), 'fasta', 'genome.fa'))
        self.assertEqual(r.tgz_bn(), "refdata-GRCh38-2.1.0.tar.gz")
        self.assertEqual(r.remote_url(), os.path.join(TenxApp.config['TENX_REMOTE_REFS_URL'], r.tgz_bn()))

    @patch('subprocess.check_call')
    def test2_download_no_reference(self, test_patch):
        test_patch.return_value = 1
        r = reference.TenxReference(name='refdata-GRCh38-2.1.0')
        self.assertIsNotNone(r)

        err = io.StringIO()
        sys.stderr = err

        with self.assertRaisesRegex(Exception, 'Failed to download reference'):
            reference.download(r)
        self.assertTrue(os.path.exists(r.references_directory()))
        sys.stderr = sys.__stderr__

    @patch('subprocess.check_call')
    def test3_download(self, test_patch):
        test_patch.return_value = 1

        r = reference.TenxReference(name='refdata-GRCh38-2.1.0')
        self.assertIsNotNone(r)
        os.makedirs(r.directory())
        genome_fasta_fn = r.genome_fasta_fn()
        os.makedirs( os.path.dirname(genome_fasta_fn) )
        with open(genome_fasta_fn, "w") as f: f.write(">SEQ1\nATGC")

        err = io.StringIO()
        sys.stderr = err

        reference.download(r)
        self.assertTrue(os.path.exists(r.directory()))
        self.assertTrue(os.path.exists(r.genome_fasta_fn()))
        sys.stderr = sys.__stderr__

# -- TenxAppTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
