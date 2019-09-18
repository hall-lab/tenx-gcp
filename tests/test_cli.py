import subprocess, unittest

class TenxCliTest(unittest.TestCase):

    def test1_tenx(self):
        rv = subprocess.call(['tenx'])
        self.assertEqual(rv, 0)

    # ALIGNMENT
    def test2_tenx_alignment(self):
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

    # COMPUTE
    def test2_tenx_compute(self):
        rv = subprocess.call(['tenx', 'compute'])
        self.assertEqual(rv, 0)

    def test2_tenx_compute_list_templates(self):
        rv = subprocess.call(['tenx', 'compute', 'list-templates', '--help'])
        self.assertEqual(rv, 0)
        rv = subprocess.call(['tenx', 'compute', 'list-templates'])
        self.assertEqual(rv, 0)

    def test2_tenx_compute_submit(self):
        rv = subprocess.call(['tenx', 'compute', 'submit', '--help'])
        self.assertEqual(rv, 0)
        rv = subprocess.call(['tenx', 'compute', 'submit'])
        self.assertEqual(rv, 2)

    # READS
    def test3_tenx_reads(self):
        rv = subprocess.call(['tenx', 'reads'])
        self.assertEqual(rv, 0)

    def test3_tenx_reads_download(self):
        rv = subprocess.call(['tenx', 'reads', 'download', '--help'])
        self.assertEqual(rv, 0)
        rv = subprocess.call(['tenx', 'reads', 'download'])
        self.assertEqual(rv, 2)

    def test4_tenx_util(self):
        rv = subprocess.call(['tenx', 'util'])
        self.assertEqual(rv, 0)

    def test4_tenx_reads_download(self):
        rv = subprocess.call(['tenx', 'util', 'calculate-compute-metrics', '--help'])
        self.assertEqual(rv, 0)
        rv = subprocess.call(['tenx', 'util', 'calculate-compute-metrics'])
        self.assertEqual(rv, 2)

    # REFERENCE
    def test2_tenx_ref(self):
        rv = subprocess.call(['tenx', 'ref'])
        self.assertEqual(rv, 0)

    def test2_tenx_ref_download(self):
        rv = subprocess.call(['tenx', 'ref', 'download', '--help'])
        self.assertEqual(rv, 0)
        rv = subprocess.call(['tenx', 'ref', 'download'])
        self.assertEqual(rv, 2)

# -- TenxCliTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
