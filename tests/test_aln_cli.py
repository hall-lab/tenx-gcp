import subprocess, unittest

class TenxAlnCliTest(unittest.TestCase):

    def test1_tenx_alignment(self):
        rv = subprocess.call(['tenx', 'aln'])
        self.assertEqual(rv, 0)

    def test2_tenx_aln_align(self):
        rv = subprocess.call(['tenx', 'aln', 'align', '--help'])
        self.assertEqual(rv, 0)
        rv = subprocess.call(['tenx', 'aln', 'align'])
        self.assertEqual(rv, 2)

    def test2_tenx_aln_pipeline(self):
        rv = subprocess.call(['tenx', 'aln', 'pipeline', '--help'])
        self.assertEqual(rv, 0)
        rv = subprocess.call(['tenx', 'aln', 'pipeline'])
        self.assertEqual(rv, 2)

    def test2_tenx_aln_upload(self):
        rv = subprocess.call(['tenx', 'aln', 'upload', '--help'])
        self.assertEqual(rv, 0)
        rv = subprocess.call(['tenx', 'aln', 'upload'])
        self.assertEqual(rv, 2)

# -- TenxAlnCliTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
