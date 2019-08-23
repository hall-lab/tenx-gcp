import gzip, os, shutil, StringIO, subprocess, sys, tarfile, tempfile, unittest
from mock import patch

from .context import tenx
from tenx.app import TenxApp
from tenx import reference

class TenxAppTest(unittest.TestCase):

    def test1_reference(self):
        tenxapp = TenxApp()
        self.assertIsNotNone(TenxApp.config)
        TenxApp.config['TENX_DATA_PATH'] = tempfile.mkdtemp()
        TenxApp.config['TENX_REMOTE_URL'] = 'gs://data'
        r = reference.TenxReference(name='refdata-GRCh38-2.1.0')
        self.assertEqual(r.references_directory(), os.path.join(os.path.sep, TenxApp.config['TENX_DATA_PATH'], 'references'))
        self.assertEqual(r.directory(), os.path.join(r.references_directory(), r.name))
        self.assertEqual(r.genome_fasta_fn(), os.path.join(r.directory(), 'fasta', 'genome.fa'))
        self.assertEqual(r.tgz_bn(), "refdata-GRCh38-2.1.0.tar.gz")
        self.assertEqual(r.remote_url(), os.path.join(TenxApp.config['TENX_REMOTE_URL'], 'references', r.tgz_bn()))

    @patch('subprocess.check_call')
    def test2_download_no_reference(self, test_patch):
        test_patch.return_value = 1
        r = reference.TenxReference(name='refdata-GRCh38-2.1.0')
        self.assertIsNotNone(r)

        err = StringIO.StringIO()
        sys.stderr = err

        with self.assertRaisesRegexp(Exception, 'Failed to download reference'):
            reference.download(r)
        self.assertTrue(os.path.exists(r.references_directory()))
        sys.stderr = sys.__stderr__

    @patch('subprocess.check_call')
    def test3_download(self, test_patch):
        test_patch.return_value = 1

        r = reference.TenxReference(name='refdata-GRCh38-2.1.0')
        self.assertIsNotNone(r)
        shutil.copyfile(os.path.join('tests', 'test_reference', r.tgz_bn()), os.path.join(r.references_directory(), r.tgz_bn()))
        subprocess.call(['tar', 'zxf', os.path.join(r.references_directory(), r.tgz_bn()), '-C', r.references_directory()])

        err = StringIO.StringIO()
        sys.stderr = err

        reference.download(r)
        self.assertTrue(os.path.exists(r.directory()))
        self.assertTrue(os.path.exists(r.genome_fasta_fn()))
        sys.stderr = sys.__stderr__

# -- TenxAppTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
